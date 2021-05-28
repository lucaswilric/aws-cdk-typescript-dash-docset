# aws-cdk-typescript-dash-docset

Generate an AWS CDK Typescript docset for [Dash](https://kapeli.com/dash) or
[Zeal](https://zealdocs.org/), based on the published docs on
`docs.aws.amazon.com`

## How to use it

This code depends on Python 3, plus a number of libraries. You can install
Python with `asdf` by running `asdf install`, or you can manage that by other
means.

1. Install a compatible version of Python:
   
   ```bash
   $ asdf install
   ```
   
2. Install packages:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Run `./gen_docset.sh`

## How it works

### Step 1: Scrape all the docs from Amazon (Bash script)

This step uses `wget --recursive` to find and download all the docs from
`docs.aws.amazon.com`. It may take a while.

### Step 2: Munge the docs into a Dash-friendly form (Python script)

There are a few things going on here:

* Removing unwanted tags from the HTML (for example, we don't need `<script>`
  tags or unsightly headers in Dash)
* Building up an index of all the programming constructs for Dash to search
  through (as per the instructions
  [here](https://kapeli.com/docsets#dashDocset))
* Structuring it all as a `.docset` folder, ready for Dash to import
