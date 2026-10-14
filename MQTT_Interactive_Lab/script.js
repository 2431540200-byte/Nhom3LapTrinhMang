const $ = (s) => document.querySelector(s);
let nextId = 4;
let subs = [
  {id:1,name:"Màn hình nhiệt độ",topic:"classroom/temperature",received:0},
  {id:2,name:"Bảng điều khiển",topic:"classroom/#",received:0},
  {id:3,name:"Cảm biến độ ẩm",topic:"classroom/humidity",received:0}
];
const qosText = {
  "0":"Gửi tối đa một lần; message có thể bị mất.",
  "1":"Đảm bảo ít nhất một lần; đôi khi có thể nhận trùng.",
  "2":"Cơ chế QoS cao nhất, hướng đến giao nhận đúng một lần giữa hai bên MQTT."
};
function toast(text){const el=$("#toast");el.textContent=text;el.classList.add("show");clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.classList.remove("show"),2500)}
function matches(filter,topic){
  const f=filter.split("/"), t=topic.split("/");
  for(let i=0;i<f.length;i++){if(f[i]==="#")return i===f.length-1;if(i>=t.length)return false;if(f[i]!=="+"&&f[i]!==t[i])return false}
  return f.length===t.length;
}
function renderSubs(){
  const root=$("#subscribers");root.replaceChildren();
  subs.forEach(s=>{
    const row=document.createElement("div");row.className="sub-card";
    const icon=document.createElement("div");icon.className="logo";icon.textContent="S";
    const info=document.createElement("div");info.className="info";
    const name=document.createElement("strong");name.textContent=s.name;
    const topic=document.createElement("small");topic.textContent=`Topic: ${s.topic} · Đã nhận: ${s.received}`;
    info.append(name,topic);
    const remove=document.createElement("button");remove.type="button";remove.className="remove";remove.textContent="Xóa";
    remove.addEventListener("click",()=>{subs=subs.filter(x=>x.id!==s.id);renderSubs();toast("Đã xóa Subscriber")});
    row.append(icon,info,remove);root.append(row);
  });
}
function animate(){
  const nodes=[$("#publisherNode"),$("#brokerNode"),$("#subscriberNode")], arrows=[$("#arrow1"),$("#arrow2")];
  nodes.forEach(n=>n.classList.remove("active"));arrows.forEach(a=>a.classList.remove("active"));
  nodes[0].classList.add("active");
  setTimeout(()=>{nodes[0].classList.remove("active");arrows[0].classList.add("active");nodes[1].classList.add("active")},220);
  setTimeout(()=>{arrows[0].classList.remove("active");nodes[1].classList.remove("active");arrows[1].classList.add("active");nodes[2].classList.add("active")},500);
  setTimeout(()=>{nodes.forEach(n=>n.classList.remove("active"));arrows.forEach(a=>a.classList.remove("active"))},1000);
}
$("#qos").addEventListener("change",e=>$("#qosInfo").textContent=qosText[e.target.value]);
$("#publishForm").addEventListener("submit",e=>{
  e.preventDefault();const topic=$("#topic").value.trim(), message=$("#message").value.trim(), qos=$("#qos").value;
  if(!topic||!message)return toast("Hãy nhập Topic và message.");
  if(topic.includes("#")||topic.includes("+"))return toast("Topic Publish không được chứa + hoặc #.");
  const recipients=subs.filter(s=>matches(s.topic,topic));recipients.forEach(s=>s.received++);
  renderSubs();animate();
  $("#empty").hidden=true;
  const log=document.createElement("div");log.className="log";
  const tag=document.createElement("span");tag.className="tag";tag.textContent="QoS "+qos;
  const body=document.createElement("div");
  const title=document.createElement("strong");title.textContent=topic;
  const msg=document.createElement("p");msg.textContent=message;
  const time=document.createElement("small");time.textContent=`${new Date().toLocaleTimeString("vi-VN")} · ${recipients.length?`Mô phỏng gửi đến ${recipients.length} Subscriber`:"Không có Subscriber phù hợp"}`;
  body.append(title,msg,time);log.append(tag,body);$("#logs").prepend(log);
  toast(recipients.length?`Đã mô phỏng gửi đến ${recipients.length} Subscriber.`:"Không có Subscriber phù hợp với Topic.");
});
$("#subForm").addEventListener("submit",e=>{
  e.preventDefault();const name=$("#subName").value.trim(),topic=$("#subTopic").value.trim();
  if(!name||!topic)return toast("Hãy nhập tên và Topic.");
  const levels=topic.split("/");
  if(levels.some((x,i)=>x.includes("#")&&!(x==="#"&&i===levels.length-1)||x.includes("+")&&x!=="+"))return toast("Topic filter dùng + theo một cấp và # ở cuối.");
  subs.push({id:nextId++,name,topic,received:0});renderSubs();$("#subName").value="";toast("Đã thêm Subscriber.");
});
$("#clear").addEventListener("click",()=>{$("#logs").replaceChildren();$("#empty").hidden=false;toast("Đã xóa nhật ký.")});
renderSubs();
