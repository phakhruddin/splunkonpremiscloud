* * *

Splunk On-Premise Cloud
=======================

![Python CI](https://github.com/dbaycoinc/splunkonpremiscloud/actions/workflows/python.yml/badge.svg)

![Terraform CI](https://github.com/dbaycoinc/splunkonpremiscloud/actions/workflows/terraform.yml/badge.svg)

[![codecov](https://codecov.io/gh/phakhruddin/splunkonpremiscloud/graph/badge.svg?token=NKHIE2HCLL)](https://codecov.io/gh/phakhruddin/splunkonpremiscloud)

![License](https://img.shields.io/github/license/phakhruddin/splunkonpremiscloud.svg)

![Contributors](https://img.shields.io/github/contributors/phakhruddin/splunkonpremiscloud.svg)

![Issues](https://img.shields.io/github/issues/phakhruddin/splunkonpremiscloud.svg)

This repository provides a foundational GitOps setup for deploying and managing Splunk Enterprise in AWS using a combination of Terraform, Python, Bash, and YAML declarative configuration files. The workflow simplifies the provisioning, configuration, and scaling of Splunk indexers, search heads, deployers, and cluster masters.

# On Premise Splunk Enterprise Deployment in AWS

This project aims to provide a robust, scalable, and high-performance design for deploying Splunk Enterprise on an on-premise cloud infrastructure. The design and implentation are based on vetted resources, industry best practices, and the latest recommendations.

Design Philosophy
-----------------

The architecture of this repository is informed by the following vetted and recommended documents:

1.  **Splunk Enterprise Deployment on AWS**  
    A technical brief outlining best practices for deploying Splunk on AWS, which has been adapted to suit on-premise cloud environments.  
    [Read the document here](https://www.splunk.com/en_us/pdfs/tech-brief/deploying-splunk-enterprise-on-aws.pdf)
    
2.  **Splunk Enterprise System Requirements**  
    Official Splunk documentation providing system requirements and recommendations for installing and running Splunk Enterprise effectively.  
    [Read the documentation here](https://docs.splunk.com/Documentation/Splunk/9.3.2/Installation/Systemrequirements?utm_source=chatgpt.com)
    
3.  **AWS Well-Architected Framework**  
    Guidance from AWS's Well-Architected Framework, focusing on building secure, high-performing, and resilient infrastructure. These principles are leveraged to inform on-premise design decisions.  
    [Explore the framework here](https://aws.amazon.com/premiumsupport/business-support-well-architected/?trk=e71ac1e0-c82d-4dcb-bcde-85de0ceae1f5&sc_channel=ps&ef_id=Cj0KCQiAsOq6BhDuARIsAGQ4-zjSV2n5gxP_kGZkO5hlp6h5Etl_fXRww-XgL4DNc6WmS2XQqcXh-fUaAkVgEALw_wcB:G:s&s_kwcid=AL!4422!3!719222313837!e!!g!!aws%20well%20architected!21852254328!176452269744&gbraid=0AAAAA-aZeIX-H4LqGMQQqBFcZlL-Sv3x8&gclid=Cj0KCQiAsOq6BhDuARIsAGQ4-zjSV2n5gxP_kGZkO5hlp6h5Etl_fXRww-XgL4DNc6WmS2XQqcXh-fUaAkVgEALw_wcB)
    
4.  **Best-in-Class Industry Standards**  
    The codebase is structured based on industry-standard best practices for open-source repositories, ensuring maintainability, extensibility, and ease of collaboration.
    

Intent and Scope
----------------

The intent of this project is not to compete with or divert from Splunk's SaaS offerings in the cloud. Instead, it aims to complement those offerings by addressing scenarios where SaaS solutions may not be viable or practical. While the focus is on Splunk Enterprise, the principles and design patterns showcased here can be applied to other applications requiring similar on-premises cloud architectures.

Features
--------

*   Modular infrastructure-as-code (Terraform) for deploying and managing Splunk Enterprise components.
*   Python scripts for Splunk configuration and API management, adhering to well-tested practices.
*   CI/CD pipelines for linting, testing, and deployment using GitHub Actions.
*   YAML-based configuration files to allow for flexible and reusable deployment setups.
*   Pre-configured monitoring and logging best practices, inspired by the AWS Well-Architected Framework.

Repository Highlights
---------------------

*   **Client-Facing Inputs**: Dedicated directories for user-provided YAML configurations.
*   **Core Engine**: Python and Bash scripts encapsulating the deployment and configuration logic.
*   **CI/CD Integration**: Automated workflows for testing, linting, and deploying updates.
*   **Documentation**: Comprehensive guides for setting up and using the repository.

Getting Started
---------------

1.  Clone this repository:
    
    ```bash
    git clone https://github.com/phakhruddin/splunkonpremiscloud.git
    ```
    
2.  Review the documentation for setup and configuration details.

Contribution Guidelines
-----------------------

Contributions are welcome! Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get involved.

License
-------

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

* * *
