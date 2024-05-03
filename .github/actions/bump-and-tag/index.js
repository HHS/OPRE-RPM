const core = require('@actions/core');
const github = require('@actions/github');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

async function run() {
    try {
        // Obtain the GitHub token from the environment variable or action input
        const token = core.getInput('custom_token', { required: false }) || process.env.GITHUB_TOKEN;
        if (!token) {
            throw new Error('GitHub token is not provided');
        }

        // Setup GitHub client with the token
        const octokit = github.getOctokit(token);

        // Setup the working directory based on the action input or default to the current workspace
        const workspace = process.env.GITHUB_WORKSPACE || '.';
        const openApiDir = core.getInput('openapi_dir', { required: false }) || '.';
        const fullPath = path.join(workspace, openApiDir);
        process.chdir(fullPath);

        // Ensure the OpenAPI file exists
        const openApiFilePath = path.join(process.cwd(), 'openapi.yml');
        if (!fs.existsSync(openApiFilePath)) {
            throw new Error(`The openapi.yml file does not exist at ${openApiFilePath}`);
        }
        const openapi = yaml.load(fs.readFileSync(openApiFilePath, 'utf8'));

        // Fetch recent commits to determine the type of version bump required
        const repo = github.context.repo;
        const branch = github.context.ref.replace('refs/heads/', '');
        const { data: commits } = await octokit.rest.repos.listCommits({
            owner: repo.owner,
            repo: repo.repo,
            sha: branch,
            per_page: 10
        });
        const messages = commits.map(commit => commit.commit.message);
        const bumpType = determineBumpType(messages);

        // Update the OpenAPI version based on commits
        const oldVersion = openapi.info.version;
        const newVersion = updateVersion(oldVersion, bumpType);
        openapi.info.version = newVersion;
        fs.writeFileSync(openApiFilePath, yaml.dump(openapi));

        // Configure Git for commit
        const repoUrl = `https://${token}@github.com/${repo.owner}/${repo.repo}`;
        execSync('git config user.name "GitHub Action"');
        execSync('git config user.email "action@github.com"');
        execSync('git add .');
        if (!core.getBooleanInput('skip_commit', { required: false })) {
            execSync(`git commit -m "Automated commit by GitHub Action: Bump version ${oldVersion} to ${newVersion}"`);
        }

        // Tagging and pushing changes
        const tagPrefix = core.getInput('tag_prefix', { required: false });
        const tagSuffix = core.getInput('tag_suffix', { required: false });
        const newTag = `${tagPrefix}${newVersion}${tagSuffix}`;
        if (!core.getBooleanInput('skip_tag', { required: false })) {
            execSync(`git tag ${newTag}`);
            core.setOutput('new_tag', newTag);
        }
        if (!core.getBooleanInput('skip_push', { required: false })) {
            execSync(`git push ${repoUrl} HEAD:${branch}`);
            if (newTag) {
                execSync('git push --tags');
            }
        }
    } catch (error) {
        core.setFailed(error.message);
    }
}

run();

function determineBumpType(messages) {
    const majorWords = core.getInput('major_wording', { required: false }).split(',').map(word => word.trim());
    const minorWords = core.getInput('minor_wording', { required: false }).split(',').map(word => word.trim());
    const patchWords = core.getInput('patch_wording', { required: false }).split(',').map(word => word.trim());
    const preReleaseWords = core.getInput('rc_wording', { required: false }).split(',').map(word => word.trim());

    let bumpType = 'patch'; // Default to patch if no other conditions are met
    if (messages.some(msg => preReleaseWords.some(word => msg.includes(word)))) {
        bumpType = 'prerelease';
    }
    if (messages.some(msg => patchWords.some(word => msg.includes(word)))) {
        bumpType = 'patch';
    }
    if (messages.some(msg => minorWords.some(word => msg.includes(word)))) {
        bumpType = 'minor';
    }
    if (messages.some(msg => majorWords.some(word => msg.includes(word)))) {
        bumpType = 'major';
    }
    return bumpType;
}

function updateVersion(oldVersion, bumpType) {
    let parts = oldVersion.split('.').map(x => parseInt(x, 10));
    switch (bumpType) {
        case 'major':
            parts[0] += 1;
            parts[1] = 0;
            parts[2] = 0;
            break;
        case 'minor':
            parts[1] += 1;
            parts[2] = 0;
            break;
        case 'patch':
            parts[2] += 1;
            break;
        case 'prerelease':
            parts[2] += 1; // Adjust this according to how you handle pre-release versions
            break;
    }
    return parts.join('.');
}
