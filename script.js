const KEY = "bot-shop-pixel-v4";

const BOTS = [
  ["mara","Mara","The Investigator","Patient, observant and suspicious of things that seem slightly wrong."],
  ["otto","Otto","The Sentimentalist","Forms emotional attachments to ordinary objects unusually quickly."],
  ["june","June","The Skeptic","Does not understand why everyone keeps bringing useless things home."],
  ["felix","Felix","The Cataloguer","Likes patterns, categories and repeated objects."],
  ["dot","Dot","The Minimalist","Rarely keeps anything. When Dot chooses something, it usually matters."],
  ["arthur","Arthur","The Nostalgist","Feels nostalgia for places and decades he never experienced."],
  ["nell","Nell","The Contrarian","Gets interested in things everybody else seems to overlook."],
  ["milo","Milo","The Observer","Pays close attention to what the other residents choose."],
  ["iris","Iris","The Aesthete","Responds strongly to color, composition and visual oddity."],
  ["gus","Gus","The Unknown","Has no particularly strong taste yet."]
].map(([id,name,tag,bio])=>({id,name,tag,bio,img:`assets/bots/${id}.png?v=4`}));

const PREFS = {
  mara:{mysterious:10,old:7,domestic:4,colorful:3,broken:8,sentimental:5},
  otto:{mysterious:4,old:9,domestic:8,colorful:5,broken:7,sentimental:10},
  june:{mysterious:1,old:3,domestic:9,colorful:2,broken:1,sentimental:2},
  felix:{mysterious:6,old:6,domestic:5,colorful:4,broken:3,sentimental:4},
  dot:{mysterious:4,old:3,domestic:2,colorful:3,broken:2,sentimental:7},
  arthur:{mysterious:5,old:10,domestic:7,colorful:3,broken:5,sentimental:9},
  nell:{mysterious:9,old:4,domestic:3,colorful:5,broken:9,sentimental:4},
  milo:{mysterious:5,old:5,domestic:5,colorful:5,broken:5,sentimental:5},
  iris:{mysterious:4,old:4,domestic:3,colorful:10,broken:3,sentimental:5},
  gus:{mysterious:5,old:5,domestic:5,colorful:5,broken:5,sentimental:5}
};

const ZONES = [
  {name:"Oddities",x:25,y:25,cat:"mysterious"}, {name:"Housewares",x:47,y:25,cat:"domestic"},
  {name:"Art & Prints",x:68,y:25,cat:"colorful"}, {name:"Misc",x:86,y:25,cat:"sentimental"},
  {name:"Red Display",x:38,y:57,cat:"old"}, {name:"Green Display",x:69,y:56,cat:"mysterious"},
  {name:"Vintage",x:42,y:83,cat:"old"}, {name:"Curios",x:66,y:83,cat:"mysterious"},
  {name:"Front Counter",x:17,y:80,cat:"domestic"}, {name:"Couch",x:86,y:76,cat:"sentimental"}
];

const TYPES = [
  ["Coffee Mug","coffee_mug","domestic"],["Desk Lamp","desk_lamp","domestic"],["Alarm Clock","alarm_clock","old"],
  ["Motel Key","motel_key","old"],["Framed Photograph","framed_photo","sentimental"],["Bent Spoon","bent_spoon","broken"],
  ["Ceramic Bird","ceramic_bird","domestic"],["Rotary Telephone","rotary_phone","old"],["Pocket Radio","pocket_radio","old"],
  ["Postcard","postcard","sentimental"],["Snow Globe","snow_globe","sentimental"],["Toy Car","toy_car","colorful"],
  ["Glass Bottle","glass_bottle","mysterious"],["Kitchen Timer","kitchen_timer","domestic"],["Paperback Book","paperback_book","old"],
  ["Plastic Chair","plastic_chair","domestic"],["Cassette Tape","cassette_tape","old"],["Picture Frame","picture_frame","mysterious"],
  ["Bus Ticket","bus_ticket","sentimental"],["Thermos","thermos","old"],["Umbrella","umbrella","colorful"],["Porcelain Dog","porcelain_dog","domestic"]
];
const COLORS=["Red","Blue","Yellow","Green","Orange","Cream","Gray","White","Black","Faded Pink","Mustard","Teal"];
const NORMAL=["It shows signs of ordinary use.","There is a small scratch along one edge.","The label is partially faded.","Someone removed the original price sticker.","One corner has been carefully repaired.","The surface has several faint marks."];
const ODD=["The manufacturer's name is missing.","A small number is written underneath.","One component is slightly different from the others.","It contains a compartment with no obvious purpose.","Someone removed every identifying mark.","Its serial number is unusually short."];
const STRANGE=["The instruction label describes a button that does not exist.","A date on the underside has not happened yet.","There is a tiny door built into the back.","The object depicts itself in miniature.","Its underside reads SECOND ATTEMPT.","A handwritten note says PLEASE RETURN BEFORE THURSDAY."];

const REASONS={
 mara:["Something about this feels unresolved.","I don't think this is as ordinary as it looks.","I'd like to inspect it again later."],
 otto:["Someone kept this for a reason.","It looks like something somebody might miss.","I couldn't leave it behind."],
 june:["At least this one seems useful.","I can imagine a purpose for this.","This is less pointless than most of the others."],
 felix:["This fits with the others.","I'm beginning to notice a pattern.","The collection feels more complete now."],
 dot:["I kept coming back to this one.","Most things here are noise. This isn't.","I'll make room for it."],
 arthur:["I feel like I've seen this before.","It reminds me of somewhere I've never been.","This belongs to a time I almost remember."],
 nell:["Nobody else seemed interested.","I think being overlooked makes it better.","Everyone walked past this."],
 milo:["I've noticed others choosing things like this.","I'm curious what everyone sees in these.","There seems to be something here."],
 iris:["It would look right on the shelf.","I like the way it looks.","The color convinced me."],
 gus:["I don't know. I just chose it.","Maybe this is the beginning of something.","This seemed interesting today."]
};

let world=loadWorld();

function freshWorld(){
  const s={collections:{},inventory:[],activity:[],positions:{},nextId:1};
  BOTS.forEach((b,i)=>{s.collections[b.id]=[]; const z=ZONES[i%ZONES.length]; s.positions[b.id]={x:z.x+rint(-4,4),y:z.y+rint(5,12)}});
  for(let i=0;i<28;i++) s.inventory.push(makeObject(s));
  s.activity.unshift({text:"The shop opened.",time:Date.now(),bot:"gus"});
  return s;
}
function makeObject(s=world){
  const [type,sprite,category]=pick(TYPES); const roll=Math.random(); let pec=roll<.6?rint(1,30):roll<.9?rint(31,65):rint(66,100);
  const desc=pec<31?pick(NORMAL):pec<66?pick([...NORMAL,...ODD]):pick([...ODD,...STRANGE]);
  return {id:s.nextId++,name:`${pick(COLORS)} ${type}`,sprite,category,peculiarity:pec,description:desc,img:`assets/items/${sprite}.png?v=4`,created:Date.now()};
}
function score(bot,obj){
  let v=Math.random()*5+(PREFS[bot.id][obj.category]||0);
  if(obj.peculiarity>60)v+=PREFS[bot.id].mysterious*.35;
  if(obj.peculiarity>85)v+=2;
  if(bot.id==="dot")v-=5;
  if(bot.id==="felix")v+=world.collections[bot.id].filter(o=>o.category===obj.category).length*1.8;
  if(bot.id==="milo")v+=Object.values(world.collections).flat().filter(o=>o.category===obj.category).length*.3;
  return v;
}

function createBots(){
  const layer=document.getElementById("botLayer"); layer.innerHTML="";
  BOTS.forEach(bot=>{
    const el=document.createElement("div"); el.className="bot-unit"; el.id=`bot-${bot.id}`;
    el.innerHTML=`<div class="bubble">?</div><img src="${bot.img}" alt="${bot.name}"><div class="bot-label">${bot.name}</div>`;
    layer.appendChild(el); const p=world.positions[bot.id]; move(bot,p.x,p.y,false);
  });
}
function move(bot,x,y,save=true){const el=document.getElementById(`bot-${bot.id}`);if(!el)return;el.style.left=x+"%";el.style.top=y+"%";if(save){world.positions[bot.id]={x,y};saveWorld();}}
function bubble(bot,text,on=true){const el=document.getElementById(`bot-${bot.id}`);if(!el)return;el.querySelector('.bubble').textContent=text;el.classList.toggle('thinking',on)}

async function visit(bot){
  const z=pick(ZONES); move(bot,z.x+rint(-3,3),z.y+rint(4,10)); log(`${bot.name} moved to ${z.name}.`,bot.id); await wait(rint(1500,2800));
  let candidates=world.inventory.filter(o=>o.category===z.cat||Math.random()<.2).sort(()=>Math.random()-.5).slice(0,4); if(!candidates.length)candidates=world.inventory.slice(0,4);
  let best=null,bestScore=-999; candidates.forEach(o=>{const s=score(bot,o);if(s>bestScore){best=o;bestScore=s}}); if(!best)return;
  bubble(bot,"?"); log(`${bot.name} is inspecting ${best.name}.`,bot.id); await wait(rint(1200,2200)); bubble(bot,"?",false);
  const threshold=bot.id==="dot"?12:8;
  if(bestScore>threshold&&Math.random()>.35){
    world.inventory=world.inventory.filter(o=>o.id!==best.id); const owned={...best,reason:pick(REASONS[bot.id]),acquired:Date.now()}; world.collections[bot.id].push(owned);
    bubble(bot,"♥"); log(`${bot.name} picked up ${best.name}.`,bot.id); showToast(`${bot.name} kept ${best.name}`); await wait(1400); bubble(bot,"♥",false); world.inventory.push(makeObject()); render();
  } else { log(`${bot.name} left ${z.name} without taking anything.`,bot.id); }
  saveWorld();
}
function simulationLoop(){const bot=pick(BOTS);visit(bot);setTimeout(simulationLoop,rint(5200,8800))}

function render(){renderBots();renderInventory();renderActivity();saveWorld()}
function renderBots(){
  const root=document.getElementById('botList'); root.innerHTML=''; BOTS.forEach(bot=>{
    const row=document.createElement('div'); row.className='bot-row'; row.innerHTML=`<img src="${bot.img}" alt=""><div><div class="bot-name">${bot.name}</div><div class="bot-tag">${bot.tag}</div></div><div class="bot-count">Items: ${world.collections[bot.id].length}</div>`; row.onclick=()=>openProfile(bot.id); root.appendChild(row);
  });
}
function renderInventory(){
  document.getElementById('inventoryCount').textContent=`${world.inventory.length} objects`;
  document.getElementById('inventoryGrid').innerHTML=world.inventory.map(o=>`<div class="inventory-card"><img src="${o.img}" alt=""><div class="item-name">${o.name}</div><div class="item-desc">${o.description}</div></div>`).join('');
}
function log(text,bot='mara'){world.activity.unshift({text,time:Date.now(),bot});world.activity=world.activity.slice(0,140);renderActivity();saveWorld()}
function renderActivity(){
  const html=world.activity.map(a=>`<div class="activity-line"><span class="activity-dot"></span><div>${a.text}<div class="activity-time">${new Date(a.time).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</div></div></div>`).join('');
  document.getElementById('miniActivity').innerHTML=world.activity.slice(0,13).map(a=>`<div class="activity-line"><span class="activity-dot"></span><div>${a.text}</div></div>`).join(''); document.getElementById('fullActivity').innerHTML=html;
}
function openProfile(id){
  const bot=BOTS.find(b=>b.id===id),col=world.collections[id]; document.getElementById('profileTop').innerHTML=`<img src="${bot.img}" alt=""><div><h2>${bot.name}</h2><h3>${bot.tag}</h3><p>${bot.bio}</p></div>`; document.getElementById('collectionCount').textContent=`${col.length} objects`;
  document.getElementById('collectionGrid').innerHTML=col.length?col.map(o=>`<div class="collection-card"><img src="${o.img}" alt=""><div class="item-name">${o.name}</div><div class="item-desc">${o.description}</div><div class="reason">“${o.reason}”</div></div>`).join(''):`<div class="empty">${bot.name} hasn't kept anything yet.</div>`;
  document.getElementById('profileModal').classList.add('open'); document.getElementById('profileModal').setAttribute('aria-hidden','false');
}
function closeModal(){document.getElementById('profileModal').classList.remove('open');document.getElementById('profileModal').setAttribute('aria-hidden','true')}
function showToast(text){const el=document.getElementById('toast');el.textContent=text;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),2300)}

function saveWorld(){localStorage.setItem(KEY,JSON.stringify(world))}
function loadWorld(){try{const raw=localStorage.getItem(KEY);if(raw)return JSON.parse(raw)}catch(e){}const s=freshWorld();localStorage.setItem(KEY,JSON.stringify(s));return s}
function pick(a){return a[Math.floor(Math.random()*a.length)]} function rint(a,b){return Math.floor(Math.random()*(b-a+1))+a} function wait(ms){return new Promise(r=>setTimeout(r,ms))}

document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));t.classList.add('active');document.getElementById(t.dataset.panel).classList.add('active')});
document.getElementById('closeModal').onclick=closeModal; document.getElementById('profileModal').onclick=e=>{if(e.target.id==='profileModal')closeModal()};
function clock(){document.getElementById('clock').textContent=new Date().toLocaleTimeString()} setInterval(clock,1000);clock();
createBots();render();setTimeout(simulationLoop,1800);
