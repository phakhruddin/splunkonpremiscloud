# Project Roadmap

This document outlines the planned features, enhancements, and milestones for the project. The roadmap is designed to provide transparency into the project's direction and to encourage contributions from the community.

---

## **Goals and Vision**

The goal of this project is to create a robust and modular infrastructure and configuration management solution for Splunk environments using Terraform, Python, and Bash, with GitHub Actions for CI/CD. The vision is to:
- Automate infrastructure deployment on AWS.
- Simplify Splunk configuration management.
- Foster a strong open-source community for extensibility and scalability.

---

## **Milestones**

### **Phase 1: Foundation Setup (Current Phase)**

#### **Infrastructure (Terraform)**
- [x] Develop AWS VPC module for private, public, and data subnets.
- [x] Create Terraform modules for:
  - [x] Network ACLs.
  - [x] Security Groups.
- [x] Add support for configuring EC2 instances for Splunk indexers, search heads, and heavy forwarders.
- [x] Configure S3 buckets for Splunk storage backend.
- [x] Implement state management with S3 and DynamoDB.

#### **Splunk Configuration (Python)**
- [x] Develop Python utilities for managing Splunk indexes, saved searches, and alerts via the REST API.
- [x] Add support for dynamic YAML-based Splunk configurations.
- [x] Create Python scripts for managing EC2 instance roles and lifecycle.

#### **CI/CD (GitHub Actions)**
- [x] Implement Terraform workflows for linting, validation, and deployment.
- [x] Create Python workflows for linting, testing, and deployment.

---

### **Phase 2: Advanced Automation**

#### **Infrastructure (Terraform)**
- [ ] Add support for auto-scaling Splunk components (e.g., indexers, search heads).
- [ ] Integrate Terraform modules for:
  - [ ] AWS Lambda for event-driven Splunk data ingestion.
  - [ ] Route 53 for DNS configuration.

#### **Splunk Configuration (Python)**
- [ ] Add support for:
  - [ ] Splunk role-based access control (RBAC).
  - [ ] Managing Splunk apps via the Splunk App Management API.
- [ ] Create Python modules for dynamic Splunk cluster configuration.

#### **Supplementary Tools**
- [ ] Develop Bash scripts for:
  - [ ] Automated Splunk binary updates.
  - [ ] Backup and restoration of Splunk configurations.
- [ ] Implement Python-based dashboards for monitoring deployment metrics.

---

### **Phase 3: Monitoring and Observability**

#### **Infrastructure (Terraform)**
- [ ] Deploy CloudWatch alarms and metrics for Splunk node monitoring.
- [ ] Add support for centralized logging using AWS CloudWatch Logs.

#### **Splunk Observability**
- [ ] Automate deployment of Splunk IT Service Intelligence (ITSI).
- [ ] Add automated Splunk dashboards for monitoring system health.

---

### **Phase 4: Community Features**

#### **Collaboration Tools**
- [ ] Develop CLI tools for easier interaction with the project (e.g., managing YAML configurations).
- [ ] Add command-line validation for Terraform plans and Python scripts.

#### **Community Growth**
- [ ] Host regular community meetings to discuss upcoming features.
- [ ] Add a contributors page to highlight major contributions.
- [ ] Offer `good first issue` tags to encourage new contributors.

---

## **Release Plan**

| Version | Features Planned                          | Expected Release |
|---------|-------------------------------------------|------------------|
| 1.0.0   | Initial release with core infrastructure, | Q1 2025          |
|         | Python utilities, and CI/CD workflows.    |                  |
| 1.1.0   | Auto-scaling and advanced Splunk configs. | Q2 2025          |
| 1.2.0   | Monitoring and observability features.    | Q3 2025          |
| 2.0.0   | CLI tools and community-driven features.  | Q4 2025          |

---

## **How to Contribute**
If you'd like to contribute to any of the planned features or suggest new ideas, please:
1. Check the [Issues section](https://github.com/your-repo/issues) for ongoing discussions.
2. Review the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidance on submitting pull requests.
3. Open a new feature request or bug report if necessary.

---

## **Feedback**
Your feedback is invaluable! Join the [Discussions section](https://github.com/your-repo/discussions) to share your thoughts, feature requests, or improvements.

We look forward to your contributions and support as we build this project together!