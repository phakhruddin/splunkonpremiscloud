variable "splunk_username" {}
variable "splunk_password" {}
variable "splunk_url" {}

variable "index_names" {
  description = "List of Splunk indexes to create"
  type        = list(string)
}

variable "index_max_size" {
  description = "Maximum size for each Splunk index in MB"
  type        = number
  default     = 50000
}

variable "alerts" {
  description = "Alert configurations"
  type = map(object({
    query = string
    cron  = string
  }))
}
