
const now = new Date();
console.log('Now (ISO):', now.toISOString());
console.log('Now (local string):', now.toString());
console.log('Now (local date string):', now.toLocaleDateString());
console.log('Now (local time string):', now.toLocaleTimeString());
console.log('Timezone offset (minutes):', now.getTimezoneOffset());
