<script setup>
import { ref, onMounted, watch } from 'vue'
import TitleBar from '@/components/TitleBar.vue'
import { useDevicesStore } from '@/stores/devices'
import { storeToRefs } from 'pinia'
import ContextMenu from '@imengyu/vue3-context-menu';
import Modal from '@/components/Modal.vue';

const loopCount = ref(1);
const sdp = ref('');

const deviceStore = useDevicesStore();
const { devices } = storeToRefs(deviceStore);

onMounted(() => {
  logWindowResize();
  devicesInfoReceived(devices.value);
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
	var list2 = document.getElementById("idReceiverList");
	var list3 = document.getElementById("idSendDeviceList");
	var list4 = document.getElementById("idSenderList");
	list1.style.height = hList.toString()+"px";
	list2.style.height = hList.toString()+"px";
	list3.style.height = hList.toString()+"px";
	list4.style.height = hList.toString()+"px";
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
    const el = document.getElementById("connectButton");
    el.classList.remove('btn-outline-primary');
    el.classList.add('btn-warning');
    const response = await fetch('parameters/connectSndRcv', {
      method: "POST",
      body: JSON.stringify({receiveruuid: receiverUuid.value, senderuuid: senderUuid.value}),
      headers: {"Content-Type": "application/json"}
    });
    el.classList.remove('btn-warning');
    if (!response.ok)
    {
	    el.classList.add('btn-danger');
		setTimeout(function(){el.classList.remove('btn-danger'); el.classList.add('btn-outline-primary');},2000);
	}
    else
    {
	    el.classList.add('btn-success');
		setTimeout(function(){el.classList.remove('btn-success'); el.classList.add('btn-outline-primary');},2000);
    }
  }
}

var htmlSseSource = new EventSource("/listen")
htmlSseSource.addEventListener("deviceList", (event) => {
	const myData = JSON.parse(event.data);
	devicesInfoReceived(myData);
});

const closeableModal = ref(false);

 const onSenderContextMenu = (e, item) => {
    //prevent the browser's default menu
    e.preventDefault();
    //show our menu
    ContextMenu.showContextMenu({
      x: e.x,
      y: e.y,
      items: [
        { 
          label: "Show SDP", 
          onClick: async () => {
			const response = await fetch('parameters/getSenderJson?' + new URLSearchParams({senderuuid: item.uuid}));
			if (response.ok)
			{
			  const myJson = await response.json(); //extract JSON from the http response
			  console.log(myJson);
			  sdp.value = myJson.sdp.replace(/(\r\n|\r|\n)/g, '<br>');
			  closeableModal.value = true;
			}
			else
			{
			  alert('no response in retreiving SDP');
			}
          }
        },
      ]
    });
  }
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
      <button type="button" id="connectButton" class="btn btn-outline-primary btn-sm" :disabled="receiverUuid.length == 0 || senderUuid.length == 0" @click="connectClick">Connect</button>
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
        <ul id="idRecvDeviceList" class="list-group overflow-y-auto overflow-x-hidden">
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
        <ul id="idReceiverList" class="list-group overflow-y-auto overflow-x-hidden">
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
        <ul id="idSendDeviceList" class="list-group overflow-y-auto overflow-x-hidden">
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
        <ul id="idSenderList" class="list-group overflow-y-auto overflow-x-hidden">
          <template v-for="item in senderList">
  		    <Popper hover arrow placement="left" openDelay="500" closeDelay="100">
              <!-- <li class="list-group-item list-group-item-action" role="button" @click="senderClick(item)" :class="{ active: item.active }" @contextmenu.prevent="showSenderContextMenu($event, item)"> -->
              <li class="list-group-item list-group-item-action" role="button" @click="senderClick(item)" :class="{ active: item.active }" @contextmenu="onSenderContextMenu($event, item)">
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
  
  <!-- Modal SDP -->
  <Modal v-model="closeableModal" closeable header="SDP">
  <span v-html="sdp" />
  <!--{{ sdp }}-->
  </Modal>
	
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
  
/*	.overlay {
	  position: fixed;
	  top: 0;
	  left: 0;
	  width: 100%;
	  height: 100%;
	  background: transparent;
	  z-index: 49;
	}
	
	.overlay::before {
	  content: '';
	  position: absolute;
	  width: 100%;
	  height: 100%;
	}
	
	.overlay:hover {
	  cursor: pointer;
	} */  
  </style>
