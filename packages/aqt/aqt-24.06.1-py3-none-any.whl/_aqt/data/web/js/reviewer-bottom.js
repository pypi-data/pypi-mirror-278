"use strict";let time,timerStopped=!1,maxTime=0;function updateTime(){const e=document.getElementById("time");if(maxTime===0){e.textContent="";return}time=Math.min(maxTime,time);const t=Math.floor(time/60),i=time%60,o=String(i).padStart(2,"0"),n=`${t}:${o}`;maxTime===time?e.innerHTML=`<font color=red>${n}</font>`:e.textContent=n}let intervalId;function showQuestion(e,t){showAnswer(e),time=0,maxTime=t,updateTime(),intervalId!==void 0&&clearInterval(intervalId),intervalId=setInterval(function(){timerStopped||(time+=1,updateTime())},1e3)}function showAnswer(e,t=!1){document.getElementById("middle").innerHTML=e,timerStopped=t}function selectedAnswerButton(){const e=document.activeElement;if(e)return e.dataset.ease}
