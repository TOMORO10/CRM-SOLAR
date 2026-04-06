import fs from 'fs';
import jsdom from 'jsdom';
const { JSDOM } = jsdom;

const html = fs.readFileSync('fenoge_crm.html', 'utf-8');
const dom = new JSDOM(html, { runScripts: "dangerously" });

// If there's an error, jsdom usually throws or we can catch it
if (dom.window.document.body) {
    console.log("JSDOM loaded body successfully. Length:", dom.window.document.body.innerHTML.length);
    console.log("Global D length:", dom.window.D ? dom.window.D.length : 'undefined');
    console.log("Global data length:", dom.window.data ? dom.window.data.length : 'undefined');
} else {
    console.log("Failed to load dom");
}
