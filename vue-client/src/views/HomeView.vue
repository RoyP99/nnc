<script setup>
import { ref, onMounted, watch } from 'vue'
import TitleBar from '@/components/TitleBar.vue'
import { useDevicesStore } from '@/stores/devices'
import { storeToRefs } from 'pinia'
  
const loopCount = ref(1);

const deviceStore = useDevicesStore();
const { devices } = storeToRefs(deviceStore);

// const socket = new WebSocket('ws://' + location.host + '/echo');
// socket.addEventListener('message', ev => {
//     console.log('<<< ' + ev.data, 'blue');
// });
// socket.addEventListener("open", (ev) => {
//   socket.send('hallo');
//   socket.send('hallo2');
//   });
// console.log(socket);
      

onMounted(() => {
//	socket.send('hallo');
//	console.log(socket);
  logWindowResize();
})

function devicesInfoReceived(newDevices)
{
  console.log('devices verandert');
  recvDeviceList.value = [];
  sendDeviceList.value = [];
  for (let device of newDevices) {
  	// console.log(device)
	recvDeviceList.value.push({ text: device.label, uuid: device.uuid, description: device.description, type: device.type, active: false });
	sendDeviceList.value.push({ text: device.label, uuid: device.uuid, description: device.description, type: device.type, active: false });
  }
};

watch(devices, (newValue) => {
  devicesInfoReceived(devices.value);
},
//{ immediate: true }
)

const recvDeviceList = ref([
]);
const sendDeviceList = ref([
]);

const receiverList = ref([
]);
const senderList = ref([
]);

const receiverUuid = ref('');
const senderUuid = ref('');

function logWindowResize() 
{
	// set the logwindow height to fill the window 
    var dList = document.getElementById("itemsList");
    var topList = dList.offsetTop;
	var hList = window.innerHeight - topList - 10;
	var list1 = document.getElementById("idRecvDeviceList");
	list1.style.height = hList.toString()+"px";
}
// add listener for resize
window.onresize = logWindowResize;

const getDeviceReceivers = async (uuid) => {
  const response = await fetch('parameters/getDeviceReceivers?' + new URLSearchParams({uuid: uuid}));
  const myJson = await response.json(); //extract JSON from the http response
  receiverList.value = [];
  for (let receiver of myJson) {
    let subscription = "-";
    if (receiver.subscription.active)
      subscription = receiver.subscription.sender_id;
    receiverList.value.push({ text: receiver.label, uuid: receiver.id, description: receiver.description, format: receiver.format, transport: receiver.transport, subscription: subscription, active: false });
  };
}

const getDeviceSenders = async (uuid) => {
  const response = await fetch('parameters/getDeviceSenders?' + new URLSearchParams({uuid: uuid}));
  const myJson = await response.json(); //extract JSON from the http response
  senderList.value = [];
  for (let sender of myJson) {
    let subscription = "-";
    if (sender.subscription.active)
      subscription = sender.subscription.receiver_id;
    senderList.value.push({ text: sender.label, uuid: sender.id, description: sender.description, transport: sender.transport, subscription: subscription, active: false });
  };
}

function recvDeviceClick(item)
{
  for (let recvDevice of recvDeviceList.value)
    if (recvDevice.active)
      recvDevice.active = false;
  item.active = !item.active;
  receiverUuid.value = '';
  getDeviceReceivers(item.uuid);
}

function sendDeviceClick(item)
{
  for (let sendDevice of sendDeviceList.value)
    if (sendDevice.active)
      sendDevice.active = false;
  item.active = !item.active;
  senderUuid.value = '';
  getDeviceSenders(item.uuid);
}

function receiverClick(item)
{
  for (let receiver of receiverList.value)
    if (receiver.active)
      receiver.active = false;
  item.active = !item.active;
  receiverUuid.value = item.uuid;
}

function senderClick(item)
{
  for (let sender of senderList.value)
    if (sender.active)
      sender.active = false;
  item.active = !item.active;
  senderUuid.value = item.uuid;
}

async function connectClick()
{
  if (receiverUuid.value.length != 0 && senderUuid.value.length != 0)
  {
    const response = await fetch('parameters/connectSndRcv', {
      method: "POST",
      body: JSON.stringify({receiveruuid: receiverUuid.value, senderuuid: senderUuid.value}),
      headers: {"Content-Type": "application/json"}
    });
  }
}

var htmlSseSource = new EventSource("/listen")
htmlSseSource.addEventListener("deviceList", (event) => {
	const myData = JSON.parse(event.data);
	devicesInfoReceived(myData);
});

</script>

<template>
  <TitleBar msg = "Nmos Navigation Control" />
  <!--{{ devices }}-->
  <div class="row mt-5 ms-3 me-3">
    <div class="container rounded col-5 text-center" style="background-color: #e3f2fd;">
      Stream Received
    </div>
    <div class="col-2">
    </div>
    <div class="container rounded col-5 text-center" style="background-color: #e3f2fd;">
      Stream Send
    </div>
  </div>
  <div class="row mt-1 ms-3 me-3">
    <div class="container rounded col-2 text-center" style="background-color: #e3f2fd;">
      Device
    </div>
    <div class="col-1">
    </div>
    <div class="container rounded col-2 text-center" style="background-color: #e3f2fd;">
      Receiver
    </div>
    <div class="col-2 text-center">
      <button type="button" class="btn btn-outline-primary btn-sm" :disabled="receiverUuid.length == 0 || senderUuid.length == 0" @click="connectClick">Connect</button>
    </div>
    <div class="container rounded col-2 text-center" style="background-color: #e3f2fd;">
      Device
    </div>
    <div class="col-1">
    </div>
    <div class="container rounded col-2 text-center" style="background-color: #e3f2fd;">
      Sender
    </div>
  </div>
  <div id="itemsList">
    <div class="row mt-3 ms-3 me-3">
      <div class="container rounded col-2 text-center">
        <ul id="idRecvDeviceList" class="list-group overflow-auto">
          <template v-for="item in recvDeviceList">
  		    <Popper hover arrow placement="right" openDelay="500" closeDelay="100">
              <li class="list-group-item list-group-item-action" role="button" @click="recvDeviceClick(item)" :class="{ active: item.active }">
                {{ item.text }}
              </li>
              <template #content>
                <div class="myPopper"><h2>{{ item.text }}</h2><p>uuid: {{ item.uuid }}</p><p>description: {{ item.description }}</p><p>type: {{ item.type }}</p></div>
              </template>
            </Popper>
          </template>
        </ul>
      </div>
      <div class="col-1">
      </div>
      <div class="container rounded col-2 text-center">
        <ul id="idReceiverList" class="list-group overflow-auto">
          <template v-for="item in receiverList">
  		    <Popper hover arrow placement="left" openDelay="500" closeDelay="100">
              <li class="list-group-item list-group-item-action" role="button" @click="receiverClick(item)" :class="{ active: item.active }">
                {{ item.text }}
              </li>
              <template #content>
                <div class="myPopper">
                  <h2>{{ item.text }}</h2>                		
                  <p>uuid: {{ item.uuid }}</p>                		
                  <p>description: {{ item.description }}</p>                  	
                  <p>format: {{ item.format }}</p>     
                  <p>transport: {{ item.transport }}</p>             	
                  <p>subscription: {{ item.subscription }}</p>                		
                </div>
              </template>
            </popper>
          </template>
        </ul>
      </div>
      <div class="col-2 text-center">
      </div>
      <div class="container rounded col-2 text-center">
        <ul id="idSendDeviceList" class="list-group overflow-auto">
          <template v-for="item in sendDeviceList">
  		    <Popper hover arrow placement="right" openDelay="500" closeDelay="100">
              <li class="list-group-item list-group-item-action" role="button" @click="sendDeviceClick(item)" :class="{ active: item.active }">
                {{ item.text }}
              </li>
              <template #content>
                <div class="myPopper">                	
                  <h2>{{ item.text }}</h2>                  	
                  <p>uuid: {{ item.uuid }}</p>                  	
                  <p>description: {{ item.description }}</p>
                  <p>type: {{ item.type }}</p>                	
                </div>
              </template>
            </Popper>
          </template>
        </ul>
      </div>
      <div class="col-1">
      </div>
      <div class="container rounded col-2 text-center">
        <ul id="idSenderList" class="list-group overflow-auto">
          <template v-for="item in senderList">
  		    <Popper hover arrow placement="left" openDelay="500" closeDelay="100">
              <li class="list-group-item list-group-item-action" role="button" @click="senderClick(item)" :class="{ active: item.active }">
                {{ item.text }}
              </li>
              <template #content>
                <div class="myPopper">
                  <h2>{{ item.text }}</h2>                		
                  <p>uuid: {{ item.uuid }}</p>                		
                  <p>description: {{ item.description }}</p>                  	
                  <p>transport: {{ item.transport }}</p>             	
                  <p>subscription: {{ item.subscription }}</p>                		
                </div>
              </template>
            </popper>
          </template>
        </ul>
      </div>
    </div>  
  </div>
  
</template>

<style scoped>
  .myPopper {
    background: #e92791;
    padding: 20px;
    border-radius: 20px;
    color: #fff;
    /*font-weight: bold;*/
  }

  :deep(.popper) {
    /*background: #e92791;
    padding: 20px;
    border-radius: 20px;*/
    color: #fff;
    /*font-weight: bold;*/
	line-height: 0.5;
	text-align: left;
    /*text-transform: uppercase;*/
  }
  :deep(.popper #arrow::before) {
    background: #e92791;
  }

  :deep(.popper:hover),
  :deep(.popper:hover > #arrow::before) {
    background: #e92791;
  }
  </style>
