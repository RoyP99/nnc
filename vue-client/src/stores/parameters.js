import { ref, onMounted } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';

export const useParameterStore = defineStore('parameters', () => {
	const projects = ref([]);
	const projectSelected = ref('')
	const configurations = ref([]);
	const configurationSelected = ref('')
	const description = ref('');
	function getProjects() {
		const path = 'http://localhost:5000/parameters/projects';
	    axios.get(path)
	    	.then((res) => {
				projects.value = [];
			  	for (name of res.data.names)
			  	{
					projects.value.push(name);
			  	}
	          	projectSelected.value = res.data.selected;
	          	//console.log(projectSelected.value);
	          	//console.log(res.data);          
	        })
	        .catch((error) => {
	        	console.error(error);
	        });
	}
	function getConfigurations() {
		const path = 'http://localhost:5000/parameters/configuration';
	    axios.get(path)
	    	.then((res) => {
				configurations.value = [];
			  	for (name of res.data.names)
			  	{
					configurations.value.push(name);
			  	}
	          	configurationSelected.value = res.data.selected;
	          	//console.log(configuration.value);
	          	//console.log(res.data);          
	        })
	        .catch((error) => {
	        	console.error(error);
	        });
	}
	function getDescription() {
		const path = 'http://localhost:5000/parameters/description';
	    axios.get(path)
	    	.then((res) => {
				projects.value.names = [];
			  	for (name in res.data.names)
			  	{
					project.value.names.push(name);
			  	}
	          	description.value = res.data.description;
	          	//console.log(description.value);
	          	//console.log(res.data);          
	        })
	        .catch((error) => {
	        	console.error(error);
	        });
	}
  	function postProjectSelected() {
      	const path = 'http://localhost:5000/parameters/projectSelected';
      	axios.post(path, { 'value': projectSelected.value })
        	.then((res) => {
				getConfigurations();
				getDescription();
          		//console.log(res);
          		//console.log(res.data);          
        	})
        	.catch((error) => {
          		console.error(error);
        	});
    }
	function postConfigurationSelected() {
	    const path = 'http://localhost:5000/parameters/confSelected';
	    axios.post(path, { 'value': configurationSelected.value })
	      	.then((res) => {
	        	//console.log(res);
	        	//console.log(res.data);          
	      	})
	      	.catch((error) => {
	        	console.error(error);
	      	});
	}
  
  onMounted(() => {
  	getProjects();
	getConfigurations();
	getDescription();
  });
  
  return { projects, configurations, description, projectSelected, configurationSelected, postProjectSelected, postConfigurationSelected }
})
