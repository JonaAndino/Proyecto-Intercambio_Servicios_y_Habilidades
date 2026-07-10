const fs = require('fs');

const content = fs.readFileSync('Reportes.html', 'utf16le');
const lines = content.split('\n');

console.log('UTF-16LE check:');
lines.forEach((line, i) => {
    if (line.toLowerCase().includes('configura')) {
        console.log(`Line ${i+1}: ${line.trim()}`);
    }
    if (line.toLowerCase().includes('roles')) {
        console.log(`Line ${i+1}: ${line.trim()}`);
    }
});

const content2 = fs.readFileSync('Reportes.html', 'utf8');
const lines2 = content2.split('\n');

console.log('UTF-8 check:');
lines2.forEach((line, i) => {
    if (line.toLowerCase().includes('configura')) {
        console.log(`Line ${i+1}: ${line.trim()}`);
    }
    if (line.toLowerCase().includes('roles')) {
        console.log(`Line ${i+1}: ${line.trim()}`);
    }
});
