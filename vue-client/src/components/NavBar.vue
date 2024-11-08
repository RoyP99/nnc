<script setup>
import { ref } from "vue";
import { RouterLink } from 'vue-router'

//  <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
//	<div class="container-fluid">
//	    <a class="navbar-brand" href="/">NCC</a>
//	    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
//	      <span class="navbar-toggler-icon"></span>
//	    </button>
//	    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
//	      <div class="navbar-nav">
//			<RouterLink to="/" class="nav-link">Home</RouterLink>
//			<RouterLink to="/settings" class="nav-link">Settings</RouterLink>
//	      </div>
//	    </div>
//	    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
//	      <div class="navbar-nav ml-auto">
//	        <a class="nav-link" href="/testmodule">Test</a>
//	      </div>
//	    </div>
//	</div>
//  </nav>
//  <v-toolbar title="NCC" color="teal-lighten-4">
//  </v-toolbar>
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
	<div class="container-fluid">
	    <a class="navbar-brand" href="/">NCC</a>
	    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
	      <span class="navbar-toggler-icon"></span>
	    </button>
	    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
	      <div class="navbar-nav">
			<RouterLink to="/" class="nav-link">Home</RouterLink>
			<RouterLink to="/settings" class="nav-link">Settings</RouterLink>
	      </div>
	    </div>
	</div>
  </nav>
</template>

<style scoped>
</style>
