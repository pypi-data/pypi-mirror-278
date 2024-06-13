# Changelog

All notable changes to this project will be documented in this file. (from version 13.0.1.1.0 onwards)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [13.0.1.1.8] - 28-09-2023

### Added

- Note on contact when rgpd is accepted

## [13.0.1.1.7] - 24-08-2023

### Fiexed

- Missing property in allow promotions method

## [13.0.1.1.6] - 08-08-2023

### Added
- New endpoint to retrieve powerstations open for investment

## [13.0.1.1.5] - 05-06-2023

### Added 
- New endpoint to allow synchronization with mailchimp via mailchimp webhooks


## [13.0.1.1.4] - 29-06-2023

### Fixed
- Promotions policy endpoint to allow both subscription and unsubscription

## [13.0.1.1.3] - 09-06-2023

### Added
- Endpoint to update promotions policy of a contact

### Fixed
- Comparator of vat in login and signup to be case insensitive

## [13.0.1.1.2] - 26-04-2023

### Fixed
- User update process
- Password regex to allow symbols

## [13.0.1.1.1] - 20-04-2023

### Fixed
- Selection of contacts on signup request

## [13.0.1.1.0] - 11-04-2023

### Fixed
- Incorrect retrieval of account allocations
- Count of allocations to use correct search domain
- Naming of company users
- Location of a user
- Allocations shown based on check
- Allocation period calculation
- Firsname and lastname of users with two first names

### Removed
- Email validation on users to allow multiple emails separated by ';'