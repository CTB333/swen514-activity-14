output "amplify_app_id" {
  value = aws_amplify_app.tut_amplify_app.id
}

output "amplify_app_url" {
  value = aws_amplify_domain_association.tut_domain_association.domain_name
}