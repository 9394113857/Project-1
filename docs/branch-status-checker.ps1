# Initialize an empty array to store branch status information
$branchStatus = @()

# Loop through each branch in the local git repository
git branch --list | ForEach-Object {
    # Clean up branch name by removing the '*' symbol (if present) and extra spaces
    $branch = $_.Trim().Replace('*', '').Trim()

    # Skip empty or invalid branch names
    if ($branch -ne "") {
        # Checkout the branch temporarily to check its status
        git checkout --quiet $branch
        
        # Get the status of the branch (short format)
        $status = git status --short
        
        # Store the branch name and its status in the $branchStatus array
        # If the status is empty (clean), mark it as "Clean"; otherwise, mark it as "Modified"
        $branchStatus += [PSCustomObject]@{
            Branch = $branch
            Status = if ($status -eq "") {"Clean"} else {"Modified"}
        }
    }
}

# Calculate the maximum lengths of the branch name and status for padding in the table
$maxBranchLength = ($branchStatus | Measure-Object -Property Branch -Maximum).Maximum.Length
$maxStatusLength = ($branchStatus | Measure-Object -Property Status -Maximum).Maximum.Length

# Create a border line to separate the header and content in the table
$borderLine = "+" + ("-" * ($maxBranchLength + 2)) + "+" + ("-" * ($maxStatusLength + 2)) + "+"
Write-Host $borderLine

# Print the header row of the table, with the column names padded to match the maximum length
Write-Host ("| " + "Branch".PadRight($maxBranchLength) + " | " + "Status".PadRight($maxStatusLength) + " |")

Write-Host $borderLine

# Loop through the $branchStatus array and print each branch's information in a formatted table
$branchStatus | ForEach-Object {
    # Skip any null entries (just a safety check)
    if ($_ -ne $null) {
        Write-Host ("| " + $_.Branch.PadRight($maxBranchLength) + " | " + $_.Status.PadRight($maxStatusLength) + " |")
    }
}

# Print the final border line to close the table
Write-Host $borderLine

# OPTIONAL: If you want to automatically commit and push changes, you can add the following:

# Ensure you're on the 'raghu' branch before committing and pushing
git checkout raghu

# Stage any changes (for example, any updates to files or added content)
git add .

# Commit the changes with a message (you can modify the message to your liking)
git commit -m "Updated branch status display script and added formatted table output"

# Push the changes to the remote 'raghu' branch on origin
git push origin raghu

# OPTIONAL COMMAND (commented): You can use the following command to run this script after saving it.
# The command below runs the script by referencing its location in the `docs` folder.
# .\docs\branch-status-checker.ps1
# This command is used to execute the script from within PowerShell.
# It tells PowerShell to run the script file "branch-status-checker.ps1" located inside the "docs" folder in the current directory.
$scriptContent = @'
# Initialize an empty array to store branch status information
$branchStatus = @()

# Loop through each branch in the local git repository
git branch --list | ForEach-Object {
    # Clean up branch name by removing the '*' symbol (if present) and extra spaces
    $branch = $_.Trim().Replace('*', '').Trim()

    # Skip empty or invalid branch names
    if ($branch -ne "") {
        # Checkout the branch temporarily to check its status
        git checkout --quiet $branch
        
        # Get the status of the branch (short format)
        $status = git status --short
        
        # Store the branch name and its status in the $branchStatus array
        # If the status is empty (clean), mark it as "Clean"; otherwise, mark it as "Modified"
        $branchStatus += [PSCustomObject]@{
            Branch = $branch
            Status = if ($status -eq "") {"Clean"} else {"Modified"}
        }
    }
}

# Calculate the maximum lengths of the branch name and status for padding in the table
$maxBranchLength = ($branchStatus | Measure-Object -Property Branch -Maximum).Maximum.Length
$maxStatusLength = ($branchStatus | Measure-Object -Property Status -Maximum).Maximum.Length

# Create a border line to separate the header and content in the table
$borderLine = "+" + ("-" * ($maxBranchLength + 2)) + "+" + ("-" * ($maxStatusLength + 2)) + "+"
Write-Host $borderLine

# Print the header row of the table, with the column names padded to match the maximum length
Write-Host ("| " + "Branch".PadRight($maxBranchLength) + " | " + "Status".PadRight($maxStatusLength) + " |")

Write-Host $borderLine

# Loop through the $branchStatus array and print each branch's information in a formatted table
$branchStatus | ForEach-Object {
    # Skip any null entries (just a safety check)
    if ($_ -ne $null) {
        Write-Host ("| " + $_.Branch.PadRight($maxBranchLength) + " | " + $_.Status.PadRight($maxStatusLength) + " |")
    }
}

# Print the final border line to close the table
Write-Host $borderLine

# OPTIONAL: If you want to automatically commit and push changes, you can add the following:

# Ensure you're on the 'raghu' branch before committing and pushing
git checkout raghu

# Stage any changes (for example, any updates to files or added content)
git add .

# Commit the changes with a message (you can modify the message to your liking)
git commit -m "Updated branch status display script and added formatted table output"

# Push the changes to the remote 'raghu' branch on origin
git push origin raghu
'@

# Define the path where the script will be saved
$scriptPath = "E:\Office-projects\dedee-projects\Registration-Flow\docs\branch-status-checker.ps1"

# Save the script content to the file
$scriptContent | Out-File -FilePath $scriptPath

Write-Host "Script has been saved to $scriptPath"
