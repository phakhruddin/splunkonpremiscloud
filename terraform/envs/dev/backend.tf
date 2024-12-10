terraform {
  backend "s3" {
    bucket         = "splunk-terraform-state"
    key            = "splunk/dev/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-state-locks"
    encrypt        = true
  }
}
