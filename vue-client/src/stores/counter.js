import { ref, computed, onMounted } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0);
  const doubleCount = computed(() => count.value * 2);
  function increment() {
    count.value++
  }
  function getIncrement() {
      const path = 'http://localhost:5000/inc';
      axios.get(path)
        .then((res) => {
          count.value = res.data.count;
          //console.log(res);
          //console.log(res.data);          
        })
        .catch((error) => {

          console.error(error);
        });
    }
  function postIncrement(newValue) {
      const path = 'http://localhost:5000/incpost';
      axios.post(path, { 'myCount': newValue })
        .then((res) => {
          //console.log(res);
          //console.log(res.data);          
        })
        .catch((error) => {

          console.error(error);
        });
    }
  
  onMounted(() => {
  	getIncrement();
  });
  
  return { count, doubleCount, increment, getIncrement, postIncrement }
})
