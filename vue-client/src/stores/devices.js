import { ref, onMounted } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';

export const useDevicesStore = defineStore('devices', () => {
	const devices = ref([]);
	function getDevices() {
		const path = 'parameters/devices';
	    axios.get(path)
	    	.then((res) => {
				devices.value = [];
				devices.value = res.data;
// 			  	for (name of res.data.names)
// 			  	{
// 					projects.value.push(name);
// 			  	}
// 	          	projectSelected.value = res.data.selected;
	          	//console.log(projectSelected.value);
	          	//console.log(res.data); 
	          	//console.log(nodes.value);         
	        })
	        .catch((error) => {
	        	console.error(error);
	        });
	}
  
  onMounted(() => {
  	getDevices();
  });
  
  return { devices, getDevices }
})
