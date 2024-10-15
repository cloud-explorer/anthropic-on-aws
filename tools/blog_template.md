I am converting a video I made into a blog. The talk track for the video is 
<talk_track>
Over the past year, we've witnessed an explosive growth in generative AI applications. While many of these are chatbots designed to surface enterprise knowledge, today we're going to explore how we can harness the true power of generative AI to automate complex processes.

This exploration takes us into an exciting new era where AI systems can understand context, make decisions, and act independently. We're no longer confined to simple question-answering systems; instead, we're entering a landscape where AI becomes an increasingly capable partner in solving intricate problems and streamlining sophisticated workflows.

In this demo we will see how you can utilize some of the new concepts and application building patterns in generative AI to create an automated, intelligent mortgage application processing pipeline using the power of Foundational Models available through Amazon Bedrock.“

Let's dive into our demo. Imagine you're a mortgage lender faced with a diverse array of application documents - PDFs, scanned forms, and even photos from smart-phones. Traditionally, identifying and extracting information from these varied sources has been a significant challenge. That's where our solution comes in.

First, let's look at how we handle document recognition and data extraction. We're using a multi-modal Foundational Model that can process both text and images. Watch as I upload this mortgage application package... Notice how the system identifies each document type - the application form, driver's license, and W2.

What's remarkable is that we didn't have to train a specific model for each document type. Instead, we defined natural language instructions for what to extract from each document and in what format. The Foundational Model reads the document, understands the context, and extracts the required information.

Now, let's say we introduce a new document type  to the workflow or want to extract more information from the document. All an admin needs to do is provide a new set of instructions in plain language. There's no need for complex programming or model retraining. In this case when I turn on these option, all I am doing is adding a set of tools that is defined using natural language.

Moving on to our next feature, let's talk about how we optimize for both cost and performance. Our base model for this workflow is Anthropic's Claude 3.0 Haiku. It's one of the fastest and most affordable models in its category, perfect for quick, routine tasks.

However, for more complex jobs, we seamlessly switch to more powerful models. For instance, when we need to classify a multi-page application package, we use Claude 3.5 Sonnet, which excels at visual reasoning. See how Sonnet 3.5 was able to classify each page in the package as the application, drivers license ot W2. This patterns allows application builders to choose the right tool for the job while optimizing for cost and performance.

Now, let's address a critical concern in mortgage processing: data privacy. These documents contain a wealth of personal information. In this case we see there are SSNs, bank account number, emails, etc. To protect this sensitive data, we utilize Amazon Bedrock Guardrails. It enables customers to build and customize safety, privacy, and truthfulness protections for their generative AI applications in a single solution, and works with all large language models (LLMs) in Amazon Bedrock

Let me demonstrate. I'll turn on the Guardrails now, and you'll see how it automatically redacts sensitive information as we process this application. Notice how social security numbers, bank account details, and other personal identifiers are seamlessly obscured, ensuring compliance with privacy regulations without sacrificing the efficiency of our workflow.

What's particularly powerful about this system is its adaptability. As regulations change or new privacy concerns emerge, we can easily update our Guardrails without having to overhaul the entire system.

To wrap up our demo, let's review a completed application. You can see how our system has compiled all the extracted information into a comprehensive report, making it easy for loan officers to review and make informed decisions quickly.“

This approach isn't limited to mortgage processing. The same principles can be applied to various industries, from healthcare to legal services, anywhere complex document processing and decision-making are required.

</talk_track>

OK. I have chosen the title as "Conversation to Automation: Leveraging Multi-Modal, Multi-Model AI and Tool-Use for Intelligent Workflow Automation".


Now give me an introduction for this. In this want to talk about the following. I also want to discuss multi-modal vision models and multi-model approaches to generative AI as it realtes to this use case. Give me the output in 2 paragraphs. first about general trends and how we are planning on using it

We're witnessing the future of generative AI unfolding before us. We're moving from systems that require explicit programming for every action to those that can understand context, make decisions, and act on their own. This evolution points to a future where AI becomes an increasingly capable partner in solving complex problems and automating sophisticated processes. one of the most exciting developments in this area is the integration of Foundational Models with external tools to take actions in the real world. Here we see three key approaches that represent the evolution of how we're connecting AI with practical applications:

1. Traditional applications: While not new, this approach forms the baseline for our discussion on the future of AI integration.
- It's the conventional method where developers orchestrate interactions between systems and the LLM.
- The developer has full control over the application's logic and function calls.
- The app is coded to accomplish specific tasks and knows exactly what functions to call and how to call them.
- While reliable, this method can lead to a backlog of automation needs as it requires significant development time for each new task.
- It's ideal for companies that need precise control over their processes but may struggle to keep up with rapidly changing automation demands.
  
2. Function calling: This represents a significant step forward in AI autonomy and flexibility.
- Here, we give the LLM rich descriptions of available functions, allowing it to decide what to call and with what parameters.
- It enables a single "app" to handle a full range of tasks without one-off coding for each new requirement.
- This method is perfect for those tired of manual orchestration and want to easily handle multi-step tasks without hard-coding specific flows.
- It offers more flexibility and can adapt to new scenarios more easily than traditional applications.
- However, it requires careful design of function descriptions to ensure the LLM makes appropriate choices.

3. Agents: This is where we see the most potential for future AI applications.
- In this approach, the generative AI app not only chooses which functions to call but also takes action autonomously.
- It allows for creating agents with specific instructions and available actions, enabling automation with even less coding and more flexibility.
- The agent decides what actions to take, in what order, and executes those actions autonomously.
- This approach opens up many possibilities for implementation and is still evolving, with best practices and tradeoffs yet to be fully established.
- It's ideal for scenarios where you want to leverage company knowledge and automate complex, multi-step processes with minimal human intervention.

