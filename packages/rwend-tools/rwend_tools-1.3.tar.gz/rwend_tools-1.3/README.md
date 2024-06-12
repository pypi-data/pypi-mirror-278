# rwend-tools
## Installation Instructions
```bash
pip install rwend_tools
```
## Package Structure
```bash
.
├── rwend_tools
│   ├── custom_logging.py
│   ├── google_helpers.py
│   └── utils.py
```

## Detailed Function Documentation and Usage Guide
### custom_logging
  - This module helps create custom logging and email notifications
  - Prerequisites:
    - gmail_app_pwd needs to be set/defined as an environmental variable. This should be an app password you obtain from google if you want to use the email functionality of this module.
  - Usage:
    ```python
    from doh_tools.custom_logging import set_logging, send_log_over_email
    
    log_email = 'user.email@gmail.com'
    process_id = '001'
    process_name = 'Test'

    subject_success = f'Success -- {process_id} -- {process_name} Ran'
    subject_error   = f'Error -- {process_id} -- {process_name} Failed'
    
    logger = set_logging(log_console=False, log_email=True)
    logger.info('Test')
    
    try:
        logger.info(f'First line of logging')
        logger.info(f'Second line of logging')
        logger.info(f'Third line of logging')
    
        send_log_over_email(
            logger,
            fromaddr=log_email,
            toaddr=log_email,
            subject=subject_success
        )
    except Exception as e:
        logger.info(f'Process failed with error: {e}')
        send_log_over_email(
            logger,
            fromaddr=log_email,
            toaddr=log_email,
            subject=subject_error
        )
    ```
### utils
  - This module contains assorted functions
  - html_tables_to_yaml()
      - Purpose:<br>
          Generate Data Specification yaml from html.
      
          This function takes an html file or markdown file with html-style content and creates a data specification yaml file of the same name as the input file. 
          Not much can be gleaned from an html table with regards to metadata, but table name, column name, and the actual data values should be consistently captured.
      
          Parameters:<br>
              - input_file: Path to the html or markdown input file
      
          Returns:<br>
              - Data Specification: A data specification as a yaml file
    - Usage:
     ```python
      from doh_tools.utils import html_tables_to_yaml
      
      input_path = 'sample_markdown.md'
      html_tables_to_yaml(input_path)
     ```
    
