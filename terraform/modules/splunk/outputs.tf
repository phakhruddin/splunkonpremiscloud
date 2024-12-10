output "splunk_indexes" {
  value = splunk_index.indexes[*].name
}

output "splunk_alerts" {
  value = splunk_saved_search.alerts[*].name
}
