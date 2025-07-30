Installation instructions
=========================

Make sure managed dependencies is switched off
You can also visit Cloud Code Settings to turn managed dependencies on or off at any time.

Install the Google Cloud CLI
-----------------------------

### Using Homebrew

If you are on macOS, you can install the Google Cloud CLI using Homebrew:

```bash
brew install --cask google-cloud-sdk
```

After installation, restart your terminal for the changes to take effect. You can verify the installation by running:

```bash
gcloud --version
```

### Using curl

Alternatively, you can install the Google Cloud CLI using the following command:

```bash
curl https://sdk.cloud.google.com | bash
```

Reload Visual Studio Code
(Optional) Install components that Cloud Code could use
--------------------------------------------------------

After installing the Google Cloud CLI, you may optionally install additional components that Cloud Code could use. Run the following command:

```bash
gcloud components install alpha beta skaffold minikube kubectl gke-gcloud-auth-plugin
```
