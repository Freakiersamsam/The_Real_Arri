from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import logging

@CrewBase
class HierarchicalCrew():
    """Hierarchical crew with project manager"""
    
    def __init__(self):
        # Configure logging for better error visibility
        logging.basicConfig(level=logging.INFO)
        
        try:
            # Configuration using CrewAI's LLM class
            self.llm = LLM(
                model="ollama/llama3.1:8b",
                base_url="http://localhost:11434",
                timeout=300,  # Increased timeout for hierarchical processing
                temperature=0.5,  # Lower temperature for more consistent responses
                max_tokens=8192,  # Explicit token limit
            )
            
            # Manager LLM with specific configuration for hierarchical management
            self.manager_llm = LLM(
                model="ollama/llama3.1:8b",
                base_url="http://localhost:11434",
                timeout=300,
                temperature=0.3,  # Very low temperature for manager decisions
                max_tokens=8192,  # Smaller token limit for manager responses
            )
            
            print("✅ LLM connections initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize LLM: {str(e)}")
            raise

    @agent
    def project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['project_manager'],
            llm=self.manager_llm,  # Use manager LLM for consistency
            verbose=True,
            allow_delegation=True,
            max_iter=15,  # Reduced iterations to prevent complexity
            max_execution_time=600,  # 5 minute timeout
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=13,
            max_execution_time=600,
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=14,
            max_execution_time=600,
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=14,
            max_execution_time=600,
        )

    @task
    def project_planning(self) -> Task:
        return Task(
            config=self.tasks_config['project_planning'],
            agent=self.project_manager(),
            output_file="project_plan.md",
            async_execution=False,  # Ensure synchronous execution
        )

    @task
    def research_execution(self) -> Task:
        return Task(
            config=self.tasks_config['research_execution'],
            agent=self.researcher(),
            context=[self.project_planning()],
            output_file="research_report.md",
            async_execution=False,
        )

    @task
    def analysis_execution(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_execution'],
            agent=self.analyst(),
            context=[self.research_execution()],
            output_file="analysis_report.md",
            async_execution=False,
        )

    @task
    def report_writing(self) -> Task:
        return Task(
            config=self.tasks_config['report_writing'],
            agent=self.writer(),
            context=[self.project_planning(), self.research_execution(), self.analysis_execution()],
            output_file="final_report.md",
            async_execution=False,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the hierarchical crew with improved configuration"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm=self.manager_llm,
            verbose=True,
            memory=False,  # Disable memory to avoid embedder requirements
            planning=False,  # Disable planning to simplify execution
            max_rpm=10,  # Limit requests per minute
            max_execution_time=1800,  # 30 minute total timeout
            step_callback=None,  # Remove step callbacks that might cause issues
        )

    def run_project(self, topic: str):
        """
        Run the hierarchical crew with a topic
        """
        print(f"\n🚀 Starting Hierarchical Project for: '{topic}'\n")
        
        # Validate topic
        if not topic or topic.strip() == "":
            raise ValueError("Topic cannot be empty")
        
        # Update the inputs with topic
        inputs = {'topic': topic.strip()}
        
        try:
            # Test LLM connectivity before starting
            print("🔍 Testing LLM connectivity...")
            test_response = self.llm.call("Respond with just 'OK' if you can process this request.")
            print(f"✅ LLM test response: {test_response}")
            
            # Test manager LLM connectivity
            print("🔍 Testing Manager LLM connectivity...")
            manager_test = self.manager_llm.call("Respond with just 'READY' if you can manage tasks.")
            print(f"✅ Manager LLM test response: {manager_test}")
            
            # Execute the crew with error handling
            print("🎯 Starting crew execution...")
            print("⚠️  Note: Hierarchical execution may take several minutes...")
            
            result = self.crew().kickoff(inputs=inputs)
            
            return result
            
        except Exception as e:
            print(f"❌ Error during crew execution: {str(e)}")
            print("💡 Hierarchical Crew Troubleshooting:")
            print("1. Hierarchical crews require more resources - ensure Ollama has sufficient memory")
            print("2. Consider using sequential process instead: Process.sequential")
            print("3. Check if the model supports complex reasoning required for management")
            print("4. Try reducing the number of agents or tasks")
            print("5. Increase timeout values if tasks are timing out")
            raise

    def run_sequential_fallback(self, topic: str):
        """
        Fallback method using sequential process instead of hierarchical
        """
        print(f"\n🔄 Running Sequential Fallback for: '{topic}'\n")
        
        inputs = {'topic': topic.strip()}
        
        try:
            # Create a sequential crew as fallback
            sequential_crew = Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,  # Use sequential instead
                verbose=True,
                memory=False,
                max_execution_time=1800,
            )
            
            result = sequential_crew.kickoff(inputs=inputs)
            return result
            
        except Exception as e:
            print(f"❌ Sequential fallback also failed: {str(e)}")
            raise