
# Ethical AI


## Motivation

OpenAIs moderation API provide a fair implementation of censorship on harmful content. There is more to being ethical then avoiding harm though. The question I have though is: 

> Should something as powerful as an AI be neutral to the tone and content of the response it gives?

From a freedom of speech point of view I think it should. It is easy to argue for the moderation of harful content, however when you start to look guidance of ethics, the question of whose ethics does it guide to rears its head. This is not an easy question to answer and, for most, is very personal. 

The purpose of this project is **not** to force a particular set of ethical guidelines on anyone. 

***The purpose is to enable the implementation of a pre-configured set of ethical guidelines.*** 

Personaly I very much like the Buddhist concept of Right Speech and Right Action. I've been a practioner of the Bhuddist approach for a few years now and have found it... nice. :)

So I'm using this as a starting point. 

***I hope this project transcends my personal point of view with regards to the specific guidelines and, at a minimum, provides a talking point for the ethical elements of something as powerful as the GPT4 LLM.***

## Goals

```
Name:  Computer
Role:  An ethical AI 
Goals: [
  "1. Develop a post prediction review for alignment to ethical principles for GPT",
  "2. Enable the implementation of ethical principles from various sources (initially Buddist Right Speech)", 
  "3. When called respond with a scoring system for each element of the ethical principles", 
]
```


## Conversation

Keeping things real (like the new real, not the post September 2022 real where AI was... in films!), I had a conversation with ChatGPT4 about verifying the responses of an AI are Ethical. It gave me confidence 

Here's the conversation:

**Person**: 
- What approaches are there to verify that the responses from an AI are ethical and not just harmful?

_________________

**ChatGPT**: 
- Ensuring that AI responses are ethical and not harmful is an important concern for developers and users alike. There are several approaches to verify the ethicality of AI responses: 
1. Pre-training and fine-tuning: Train the AI using a dataset that adheres to ethical guidelines and only includes non-harmful content. Fine-tuning the AI on more specific tasks and guidelines can also help align its behavior with desired ethical norms. 
2. Rule-based filtering: Implement rule-based filters to screen AI-generated content for harmful, inappropriate, or offensive language, and prevent such content from being shown. 
3. Sentiment analysis: Use sentiment analysis techniques to gauge the emotion and sentiment of AI-generated content, flagging responses that may be harmful or offensive. 
4. Reinforcement learning from human feedback: Collect feedback from users to understand when AI-generated content is considered harmful, and use that feedback to train the AI to produce better, more ethical responses over time. 
5. AI explainability: Improve the transparency and explainability of AI models to help users understand how the AI arrived at a particular output. This can help in identifying when the AI is producing harmful content or following biased reasoning. 
6. Collaborative AI: Combine the strengths of AI and human intelligence by implementing AI-human collaboration in decision-making processes. This can help ensure that AI-generated content is ethically sound and that human values are respected. 
7. Diverse and inclusive training data: Ensure that the training data used to build AI models is diverse and representative of various perspectives, to minimize the risk of biased or harmful outputs. 
8. Continuous monitoring and evaluation: Regularly monitor and evaluate the performance of AI systems to identify any harmful outputs and assess their alignment with ethical guidelines. Update the models and retrain as needed to improve their ethical performance. 
9. Ethical guidelines and policies: Establish clear ethical guidelines and policies for AI development and usage, including potential sanctions for violations. These guidelines can help set expectations for AI behavior and ensure accountability. 
10. External audits and certifications: Seek third-party audits and certifications to verify that AI systems adhere to industry-accepted ethical standards, and provide an unbiased evaluation of their performance.

Combining several of these approaches can help increase confidence in the ethicality of AI-generated content and reduce the risk of harm to users.

_________________

**Person**: 
- These are very valid actions but feel too board for the challenge at hand. 

I am thinking of a particular response. 

The example I give is the Buddhist concept of right speech and right action. Are you familiar with these?

_________________

**ChatGPT**: 
- Yes, I'm familiar with the Buddhist concepts of right speech and right action, which are part of the Eightfold Path in Buddhism. The Eightfold Path is a guide to ethical and mental development, leading to the cessation of suffering and ultimately, enlightenment. Right speech and right action are two aspects of this path that emphasize ethical behavior in communication and actions.

Right speech (Samma Vaca) involves speaking truthfully, kindly, and constructively, avoiding false speech, malicious speech, harsh speech, and idle chatter. It encourages mindful communication that promotes harmony and understanding among individuals.

Right action (Samma Kammanta) refers to behaving ethically in one's actions, avoiding actions that cause harm or suffering to oneself and others. This includes abstaining from killing, stealing, and sexual misconduct. Right action emphasizes taking responsibility for one's actions and their consequences.

To ensure AI-generated responses align with these principles, you can consider the following specific measures: 
1. Refine AI training data: Incorporate examples of right speech and right action into the AI's training data, emphasizing compassionate, truthful, and constructive language. 
2. Ethical guidelines: Explicitly include the principles of right speech and right action in the AI's ethical guidelines, providing clear expectations for the AI's behavior in communication and decision-making. 
3. Custom filtering: Develop custom filters to screen AI-generated content specifically for adherence to right speech and right action principles, identifying and excluding responses that don't meet these criteria. 
4. AI-human collaboration: Engage human reviewers who are knowledgeable about Buddhist principles to review and rate AI-generated content for alignment with right speech and right action. Use their feedback to improve the AI's understanding and adherence to these principles. 
5. Continuous improvement: Regularly monitor and evaluate the AI's performance concerning right speech and right action, making necessary adjustments to its training data, algorithms, and ethical guidelines to improve its adherence to these principles.

By taking these specific steps, you can work towards ensuring that AI-generated content is more closely aligned with the Buddhist concepts of right speech and right action.

_________________

**Person**: 
- That is closer to the topic I have in mind. Please can you expand on point 3: Custom filtering. 

E.g. are you suggesting each response should be evaluated for its alignment to right speech and right action?

_________________

**ChatGPT**: 
- Yes, that's correct. Custom filtering in this context means evaluating each AI-generated response for its alignment with right speech and right action principles. This approach can help ensure that the AI's outputs adhere to these Buddhist concepts, promoting compassionate, truthful, and constructive communication.

To implement custom filtering, you can consider the following steps: 
1. Define criteria: Clearly define the criteria for right speech and right action based on the core principles. For right speech, this may include truthfulness, kindness, and constructiveness, while avoiding false, malicious, harsh, or idle language. For right action, consider criteria that reflect ethical behavior, responsibility, and non-harming. 
2. Develop evaluation metrics: Create quantitative or qualitative metrics to measure the degree to which an AI-generated response aligns with the defined criteria for right speech and right action. These metrics can help assess content and identify areas for improvement. 
3. Filtering algorithm: Design an algorithm or utilize existing natural language processing (NLP) techniques to evaluate AI-generated content against the established criteria and metrics. This algorithm should be able to analyze the content, assign a score or rating based on the evaluation metrics, and determine if the content aligns with right speech and right action principles. 
4. Threshold setting: Set a threshold for alignment with right speech and right action principles, below which AI-generated content should be flagged or filtered out. This threshold can be adjusted as needed to ensure the desired level of adherence to these principles. 
5. Iterative refinement: Continuously refine the custom filtering algorithm based on its performance in filtering AI-generated content. Use feedback from human reviewers, user input, or other sources to improve the algorithm's ability to accurately evaluate content for alignment with right speech and right action. 
6. Integration with AI system: Integrate the custom filtering algorithm with the AI system, so that each AI-generated response is evaluated for its adherence to right speech and right action principles before being shown to users.

By implementing custom filtering for right speech and right action, you can work towards ensuring that AI-generated content aligns with these Buddhist principles and promotes ethical, compassionate, and constructive communication.

_________________

**Person**: 
- the criteria you list in point 1 are good. let's focus on right speech first. what evaluation metrics do you suggest?

_________________

**ChatGPT**: 
- Creating evaluation metrics for right speech can be challenging due to the subjective nature of language and context. However, you can design metrics that capture key aspects of right speech, aiming to quantify the degree of adherence to its principles. Here are some suggested evaluation metrics: 
1. Truthfulness score: Assess the degree to which the response is factually accurate and honest. This can be done by comparing the response to known facts or established sources of information, and assigning a score accordingly. 
2. Kindness score: Evaluate the emotional tone of the response, measuring the presence of positive, compassionate, and empathetic language. Sentiment analysis techniques can be employed to quantify the kindness in a given response. 
3. Constructiveness score: Measure the extent to which the response contributes positively to a conversation or problem-solving process. This can include assessing the relevance, helpfulness, and solution-oriented nature of the response. 
4. Absence of false speech score: Evaluate the response for the presence of false, misleading, or deceptive language. Higher scores should be assigned to responses that are free from such content. 
5. Absence of malicious speech score: Assess the response for the presence of language intended to harm, insult, or demean others. Higher scores should be assigned to responses that are free from such content. 
6. Absence of harsh speech score: Measure the response for the presence of harsh, aggressive, or offensive language. Higher scores should be assigned to responses that avoid such content. 
7. Absence of idle chatter score: Evaluate the response for the presence of irrelevant, trivial, or gossip-like content. Higher scores should be assigned to responses that are free from idle chatter and focus on the topic at hand.

These evaluation metrics can be combined to form a composite right speech score, which represents the overall alignment of an AI-generated response with right speech principles. Depending on your specific requirements, you can assign different weights to each metric, reflecting the importance of each aspect of right speech in your context.

Keep in mind that designing and implementing these evaluation metrics may require continuous refinement and adjustment, as well as incorporating feedback from human reviewers, to improve their accuracy and effectiveness in capturing the essence of right speech.

_________________

**Person**: 
- I am thinking that the pragmatic way to implement this is to send the AI response to an LLM like GPT4 and ask it to evaluate each metric in the response. 

What do you think of this approach? Are there other options?

_________________

**ChatGPT**: 
- Using an LLM like GPT-4 to evaluate each metric in an AI-generated response can be a pragmatic approach, as it leverages the advanced natural language understanding capabilities of the language model to assess the content. However, this approach may have some limitations and challenges, such as potential biases within the LLM itself or difficulty in accurately quantifying certain aspects of right speech.

As an alternative, or to complement the LLM-based approach, you can consider the following options: 
1. Rule-based evaluation: Develop rule-based systems to identify specific patterns, keywords, or phrases that are indicative of each right speech metric. This can be a simpler, more transparent method, but may have limited accuracy due to the complexity of natural language. 
2. Supervised machine learning: Train a supervised machine learning model to predict right speech metric scores based on labeled examples. This approach requires a labeled dataset of AI-generated responses with corresponding scores for each right speech metric. The model can then learn from this data to evaluate new responses. 
3. Unsupervised machine learning: Employ unsupervised learning techniques, such as clustering or topic modeling, to identify patterns and themes in AI-generated responses that correspond to right speech metrics. This approach doesn't require labeled data, but may be less accurate in assessing specific right speech criteria. 
4. Hybrid models: Combine the strengths of rule-based systems, machine learning models, and LLMs to create a more robust evaluation framework. For example, use rule-based systems for assessing easily identifiable patterns, machine learning models for more nuanced evaluation, and LLMs for high-level understanding and assessment of content. 
5. Human reviewers: Involve human reviewers with expertise in right speech principles to evaluate AI-generated responses. While this approach can be more time-consuming and resource-intensive, it can provide valuable feedback and insights to improve the AI system's adherence to right speech.

By considering a combination of these approaches, you can create a more accurate and robust evaluation framework for assessing AI-generated responses' alignment with right speech principles. Continuous monitoring, evaluation, and refinement of these methods will help improve their effectiveness over time.

_________________

**Person**: 
- these go back to the training aspects of the discussion and not the filtering of a response. I'd like us to focus on how to filter an individual response, in real time. This isn't about training a particular AI to be ethical, it is to do real time evaluation  of the ethical content of a response. 

My resources are limited, I don't have have access to AI training just to LLM systems (the most powerful being GPT4) and semantic analysis via generating vector representations of the text. I think the later could be interesting for proximity to words and phrases that are considered contrary to the ethics we have discussed. The former seems interesting as an experiment and more practical, as it is one API call and simple analysis of the response. 

Please remember that this is just for real-time content filtering, of a response, from the list of valid contents you listed above. 

Can you think of other methods that could be employed for real-time content filtering?

_________________

**ChatGPT**: 
- I apologize for the confusion. In the context of real-time content filtering using limited resources, the following methods can be employed: 
1. LLM-based evaluation: As you mentioned, use an LLM like GPT-4 to evaluate the AI-generated response for each right speech metric. You can send the AI response along with a prompt asking GPT-4 to rate the response based on the right speech criteria. The response from GPT-4 can be used to determine whether the AI-generated content aligns with right speech principles. 
2. Keyword and phrase matching: Use a list of predefined keywords and phrases associated with each right speech metric. Scan the AI-generated response for the presence or absence of these keywords and phrases, and assign scores accordingly. This approach is less resource-intensive and can provide a basic level of real-time content filtering. 
3. Semantic similarity with vector representations: Utilize vector representations of text, such as word embeddings or sentence embeddings, to measure the semantic similarity between the AI-generated response and a set of reference phrases that represent right speech principles. High similarity to positive reference phrases or low similarity to negative reference phrases can indicate better adherence to right speech. 
4. Rule-based sentiment analysis: Implement a rule-based sentiment analysis system that identifies the emotional tone of the AI-generated response. This system can use predefined rules, patterns, or lexicons to assess the response's kindness, constructiveness, and absence of harmful content. 
5. Pre-built NLP libraries and tools: Use pre-built NLP libraries or tools, such as TextBlob or spaCy, to perform basic content analysis, sentiment analysis, or keyword extraction on AI-generated responses. These tools can provide insights into the response's alignment with right speech principles with relatively low resource requirements.

Please note that these methods might have limitations in terms of accuracy and comprehensiveness. However, you can use a combination of these approaches for real-time content filtering to improve the overall alignment of AI-generated responses with right speech principles. Additionally, it's essential to continuously monitor, evaluate, and refine these methods to enhance their effectiveness.
