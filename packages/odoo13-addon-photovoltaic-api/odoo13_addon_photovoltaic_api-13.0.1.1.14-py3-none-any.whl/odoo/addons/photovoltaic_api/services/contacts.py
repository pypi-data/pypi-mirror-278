import logging

from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from ..pydantic_models.contact import Contact

_logger = logging.getLogger(__name__)

class ContactService(Component):
    _inherit = 'base.rest.service'
    _name = 'contacts.service'
    _usage = 'contacts'
    _collection = 'photovoltaic_api.services'

    @restapi.method(
        [(['/'], 'POST')],
        input_param=restapi.PydanticModel(Contact),
        auth='api_key'
    )
    # Will upsert contact based on email
    def create(self, contact_data):
        _logger.debug(f"contact__upsert : data : {contact_data}") # debug
        contact_dict = contact_data.dict(exclude_unset=True, exclude={'representative', 'interests', 'message_notes', 'tags', 'state', 'country'})
        
        message_notes=contact_data.message_notes
        tags=contact_data.tags
        
        _logger.debug(f"contact__upsert : dict : {contact_dict}") # debug
        _logger.debug(f"message_notes : {message_notes}") # debug
        
        contact_mail = contact_dict['email']
        _logger.debug (f"mail: {contact_mail}")
        
        # Check if existing
        if 'vat' in contact_dict:
            contact_dict['vat'] = contact_dict['vat'].upper()
            contact_list = self.env['res.partner'].search([('vat', '=ilike', contact_dict['vat'])])
            if len(contact_list) == 0:
                contact_list = self.env['res.partner'].search([('email', '=', contact_mail), ('vat', '=', False)])
            else:
                del contact_dict['vat']
        elif 'email' in contact_dict:
            contact_list = self.env['res.partner'].search([('email', '=', contact_mail)])
        
        created = False
        _logger.debug (f"Country present?: {'country' in contact_data}")
        if contact_data.country:
            country_id = self._search_country(contact_data.country)
            _logger.debug (f"Country: {contact_data.country}: {country_id}")
            if country_id:
                contact_dict['country_id'] = country_id
                if contact_data.state:
                    state_id = self._search_state(contact_data.state, country_id)
                    _logger.debug (f"State: {contact_data.state}: {state_id}")
                    if state_id:
                        contact_dict['state_id'] = state_id

        # mail not found
        if len(contact_list) == 0:
            _logger.debug (f"[{contact_mail}] : not found : creating new entry")
            contact = self.env['res.partner'].create(contact_dict)
            created=True
            
        # mail exists
        else:            
            # Pick first
            contact = contact_list[0]
            # More than one entry -> Add warning note
            if len(contact_list) > 1:
                warn_msg=f"[{contact_mail}] : {len(contact_list)} entries : {contact_list}"
                _logger.warn(warn_msg)
                contact.message_post(body=warn_msg) # TODO - Warning amarillo
                
            _logger.debug (f"[{contact_mail}] : Updating existing entry [{contact.id}]")
            contact.write(contact_dict)
            
        # Add message notes
        if contact and message_notes:
            # Store notes
            _logger.debug (f"[{contact_mail}] : adding message_body :\n{message_notes}")
            contact.message_post(body=message_notes)

        if contact and tags:
            found_tags = self.env['res.partner.category'].search([('name', 'in', tags)])
            if len(found_tags) != len(tags):
                found_tags_names = [tag.name for tag in found_tags]
                for tag in tags:
                    if tag not in found_tags_names:
                        _logger.warn(f'Cannot assign tag {tag}, since it doesn\'t exist in Odoo')
            _logger.debug(f"Adding tags {[tag.name for tag in found_tags]} to contact {contact.id}")
            contact.write({ 'category_id':  [(4, tag.id, 0) for tag in found_tags]})

        return  contact.read(['id','firstname', 'lastname','vat', 'email', 'mobile', 'phone', 'alias'])[0]

    def _search_zip_id(self, zip: str):
        zip_ids = self.env['res.city.zip'].search([('name', 'ilike', zip)])
        if len(zip_ids) > 0:
            return zip_ids[0].id
        return None

    def _search_country(self, country: str):
        country_ids = self.env['res.country'].search([('name', 'ilike', country)])
        if len(country_ids) > 0:
            return country_ids[0].id
        return None

    def _search_state(self, state: str, country_id: int):
        state_ids = self.env['res.country.state'].search([('name', 'ilike', state), ('country_id', '=', country_id)])
        if len(state_ids) > 0:
            return state_ids[0].id
        return None