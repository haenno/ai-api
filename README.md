# AI-API

Paper and resources for a university exam on building an API to access an AI application. For the final paper see: <https://github.com/haenno/ai-api/blob/main/00-documentation/document.pdf>. A running instance of the solution can be found here <https://ai-api.tstsrv.de/>.

## Subfolders

There are serveral subfolders in order of the development of this paper:

- **00-documentation:** The paper itself including the LaTeX source and build scripts.
- **10-example-ai-app:** A simple AI application (a chatbot) based on this tutorial: <https://github.com/python-engineer/pytorch-chatbot>.
- **20-prepared-ai-app:** A futher developed version of the AI application, callable with parameters from console or directly from other Python scripts.
- **30-django-base-install:** A base installation of Django with all needed packages for a REST API including the chatbot/AI application.
- **40-vue-axios-webpage:** A Frontend for the REST API based on Vue.js and Axios.
- **50-docker-deployment:** Final stage as a ``docker-comose.yaml`` with everything put together for easy deployment.
