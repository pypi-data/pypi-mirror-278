# Shining-Brain

Shining-Brain is an innovative ETL tool designed to streamline the process of extracting data from
Excel files, transforming it to meet the necessities, and loading it into a MySQL database. Targeted
at data analysts, this tool aims to aid data analysts quickly build new visualization by using
multiple data entities, offering tailored data processing capabilities to enhance decision-making
processes.

## Background

Developed out of necessity in a data analyzing setting, Shining-Brain addresses the redundant
steps to building a new visualization for making a decision and people who previously relied on
manual data extraction and complex Excel manipulations to generate actionable insights.
Shining-Brain automates these processes, reducing error margins and improving operational
efficiency.

## Technical Overview

### Architecture

Shining-Brain employs a modular architecture, with components dedicated to data extraction,
transformation, and loading (ETL). It seamlessly integrates with existing IT infrastructure,
enabling users to configure and execute data workflows efficiently.

### Technology Stack

- **Data Extraction**: Custom scripts in Python with openpyxl for Excel file handling
- **Data Transformation**: Pandas for data manipulation and analysis
- **Data Loading**: SQLAlchemy for database interaction and mysql-connector-python for MySQL
  integration
- **Configuration**: YAML for easy-to-manage project settings
- **Visualization**: Integration with Grafana for data visualization and reporting

### Getting Started

#### Installation

Ensure you have Python 3.6+ installed, then clone the repository and install the dependencies:

```shell
git clone https://github.com/engtecmat/my_github.git
cd shining-brain
pip install -r requirements.txt
```

#### Configuration

Edit the `application.yaml` file in the `$USER_HOME/.shining-brain` directory to specify your
projects and database settings.

#### application.yaml

The application specifies the work directory under `$USER_HOME/.shinning-brain`, it loads the
application.yaml to find out how many projects need to process based on each project's own
configuration. The `projects` attribute is the root element, it includes 4 children attributes:
`name`, `directory`, `database`, and `files`.

##### Top-Level Structure

**projects:** array, required

A list of projects, each with its unique setting and configurations.

##### Project Details

**name:** string, not required, default None

The name of the project. This is a unique identifier used to reference with the project.

**directory:** string, required

The local directory path where the project files are stored.

##### Database Configuration

**database:** object, required

A nested structure that contains database connection details.

**database.host:** string, required

The IP address or hostname of the database server.

**database.schema:** string, required

The specific database schema to be used for operations.

**database.user:** string, required

The username for authentication with the database.

**database.password:** string, required

The password for authentication with the database.

##### Files Configuration

**files:** array, not required, default None

A list of file-related configurations, where each item represents a file to be processed or
managed.

**filename:** string, required

The name of the file to which following configurations will apply.

**wrangle-rules:** array, required

A list of operations or transformations to be applied to the data with the files.

**column:** string, required

Specifies the column to which the rule applies.

**operation:** string, required

Defines the type of operation to perform on the date (e.g., "contains").

**values:** array, required

A list of values that are relevant to the operations.

**actions:** array, required

A list of actions to be taken based on the rule's criteria.

**operation:** string, required

The specific action to be performed (e.g., "update")

**column:** string, not required, default current column

The column to be updated by the action.

**value:** string, required

The new value to be applied with the column.

**is-cross-join:** bool, not required, default false

A Boolean flag indicating whether a cross-join operation should be performed as part of the data
wrangling.

**filters:** object, not required, default None

Additional conditions to refine the selection of data for processing.

**color:** string, not required, default None

An example of a filter criteria, represented here as a color code.

```yaml
projects:
  - name: p1
    directory: ~/p1
    database:
      host: 127.0.0.1
      schema: test
      user: test
      password: test
    files:
      - filename: t1
        wrangle-rules:
          - column: c1
            operation: contains
            values: [ "v1", "v2" ]
            actions:
              - operation: update
                column: c1
                value: v3
              - operation: update
                column: c2
                value: v4
            is-cross-join: true
            filters:
              color: FFFF00
```

#### Usage

Run the main script to start the ETL process:

```shell
python3 main.py
```

## Dependencies

Shining-Brain relies on the following libraries:

- pandas
- sqlalchemy
- pyyaml
- openpyxl
- mysql-connector-python
- pathlib

## Release

```shell
python3 setup.py sdist
twine upload dist/*
```

## Test Coverage

```shell
coverage run -m pytest
coverage report
coverage html
```

## Advanced Features

- Data Wrangling: Define custom rules in the YAML configuration to perform complex data 
transformations.
- Automation: Schedule the ETL process to run at regular intervals, ensuring data freshness.
- Security: Encrypted database connections and secure password storage.

## Contributing

We encourage contributions to Shining-Brain. Please follow these steps to contribute:

- Fork the repository.
- Create a new branch for your feature.
- Add your changes and write unit tests.
- Submit a pull request with a detailed description of your changes.
 
## FAQs and Troubleshooting

**Q: How do I resolve connection errors with the database?**

A: Ensure your database credentials in application.yaml are correct and that your database server is accessible.

## Performance Metrics

Shining-Brain has been benchmarked to process over 10,000 records per minute, significantly reducing the time required for manual data processing.

## Future Roadmap

Planned enhancements include AI-driven data analysis features, cloud storage integration, and expanded database support.

## License

Shining-Brain is available under the MIT License. See the LICENSE file for more details.

## Contact

For support or inquiries, contact us at support@shining-brain.com.