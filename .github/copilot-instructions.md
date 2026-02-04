# GitHub Copilot Instructions

The GitHub Action workflow file `.github/workflows/depex_cicd.yml` calls our service named Depex that helps analyzing requirements and dependencies in current project and suggests a new requirements structure that has minimal impact in terms of security vulnerabilities.

The workflow will post a comment on each pull request with a report containing the results of the analysis performed by Depex: 
- If the analysis is successful, the comment will include a summary of the suggested changes to the requirements structure.
- If the analysis fails, the comment will include an error message indicating the reason for the failure

You need to read the comments posted by the workflow on pull requests and based on the information provided, suggest improvements to the requirements structure of the project. Keep in mind that the goal is to minimize security vulnerabilities while maintaining the functionality of the project. Keep your suggestions clear and actionable for the developers to implement.

