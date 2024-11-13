<script setup>
import TitleBar from '@/components/TitleBar.vue'
import { ref, onMounted } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, url } from '@vuelidate/validators';
import axios from 'axios';
import { useRouter } from 'vue-router'

const router = useRouter()

const state = ref({
  registryUrl:   ''
 });
 
const rules = {
   registryUrl: { required }
}

const validation = useVuelidate(rules, state);
validation.value.$touch();

onMounted(() => {
	getSettings();
});

function getSettings() 
{
	const path = 'parameters/settings';
    axios.get(path)
    	.then((res) => {
			//console.log(res.data);
			state.value.registryUrl   = res.data.registryUrl;
        })
        .catch((error) => {
        	console.error(error);
        });
}

function postSettings() 
{
  	const path = 'parameters/settings';
	let postValue = { 'registryUrl': state.value.registryUrl 
					}
  	axios.post(path, postValue)
    	.then((res) => {
    	})
    	.catch((error) => {
      		console.error(error);
    	});
}
async function onSubmit()
{
	const isFormCorrect = await validation.value.$validate();
	// you can show some extra alert to the user or just leave the each field to show it's `$errors`.
	if (isFormCorrect)
	{
		postSettings(); 
		router.push("/");
		//alert("correct");
	}
	// actually submit form
	
}

function checkInvalid(element)
{
	if (element.$errors.length)
	{
		return true;
	}
	return false;
}
</script>

<template>
  <TitleBar msg = "NCC Settings" />
  <form novalidate @submit.prevent="onSubmit">
    <label for="registryUrl" class="form-label m-3 mb-0">Registry Url</label>
    <div class="input-group">
      <span class="input-group-text ms-3" id="registryUrlAddon">http://example.api.com/x-nmos/query/{version}</span>
      <input
        type="text"
        class="form-control me-3"
        :class="validation.registryUrl.$invalid ? 'is-invalid' : 'is-valid'"
        id="registryUrl"
        aria-describedby="registryUrlAddon"
        v-model="validation.registryUrl.$model"
      >
      <div class="invalid-feedback"
        v-for="error of validation.registryUrl.$errors" :key="error.$uid">
        {{ error.$message }}
      </div>
    </div>
    <button type="submit" class="btn btn-primary m-3" :disabled="validation.$invalid">Submit</button> 
  </form>
</template>

<style>
</style>
