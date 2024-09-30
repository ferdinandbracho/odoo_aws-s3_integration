# Documents Manager

## Overview

This Documents Manager is an Odoo module designed to manage documents and their relationships with different models. It provides features to toggle between multiple options such as S3 storage and BlackTrust validation.

## Features

- Create document models
- Relate document models with other models
- Add flags to documents to determine if S3 storage is needed
- Add flags to documents to determine if BlackTrust validation is needed

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```

2. Navigate to the project directory:
    ```sh
    cd documents-manager
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Install the module in Odoo:
    - Copy the module folder to your Odoo addons directory.
    - Update the app list in Odoo.
    - Install the "Documents Manager" module from the Odoo app list.

## Configuration

1. Configure AWS S3 settings in Odoo:
    - Go to `Settings` > `Technical` > `Parameters` > `System Parameters`.
    - Add the following parameters:
        - `aws_access_key_id`
        - `aws_secret_access_key`
        - `aws_s3_bucket_name`

2. Configure document types:
    - Go to `Documents Manager` > `Manage Documents`.
    - Create and manage document types and their settings.

## Usage

- To manage documents, navigate to `Documents Manager` > `Documents`.
- To configure document types, navigate to `Documents Manager` > `Manage Documents`.

## Security

The module includes security settings defined in the following files:
- [security/fleet_security.xml](security/fleet_security.xml)
- [security/ir.model.access.csv](security/ir.model.access.csv)

## Views

The module provides several views to manage documents and their configurations:
- [views/views.xml](views/views.xml)
- [views/config_extender_form_view.xml](views/config_extender_form_view.xml)

