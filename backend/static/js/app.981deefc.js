(function(){"use strict";var t={3668:function(t,e,a){var n=a(9242),i=a(3396),r=a(7139),o=a.p+"img/Noodle Search.0faacc2a.jpg";const l=(0,i.uE)('<div class="title" data-v-7dd512a8><img src="'+o+'" alt="logo" style="height:100px;margin-top:auto;margin-bottom:auto;" data-v-7dd512a8><div class="text" data-v-7dd512a8><p style="color:#ffba18;line-height:16px;font-size:60px;margin-left:20px;font-family:fantasy;" data-v-7dd512a8>N</p><p style="margin-left:3px;color:#ff6a2b;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>O</p><p style="margin-left:3px;color:#0d9782;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>O</p><p style="margin-left:3px;color:#00dfc5;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>D</p><p style="margin-left:3px;color:#255fb1;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>L</p><p style="margin-left:3px;color:#992df7;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>E</p><p style="margin-left:20px;color:#c30a76;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>S</p><p style="margin-left:3px;color:#4e068d;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>E</p><p style="margin-left:3px;color:#757ff3;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>A</p><p style="margin-left:3px;color:#fe0b0b;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>R</p><p style="margin-left:3px;color:#a1a100;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>C</p><p style="margin-left:3px;color:#f72d63;line-height:16px;font-size:60px;font-family:fantasy;" data-v-7dd512a8>H</p></div></div>',1),s={class:"search-container"},f={class:"search-box"},c={key:0,class:"search-results"},p={key:1,class:"no-results"};function d(t,e,a,o,d,u){return(0,i.wg)(),(0,i.iD)(i.HY,null,[l,(0,i._)("div",s,[(0,i._)("div",f,[(0,i.wy)((0,i._)("input",{"onUpdate:modelValue":e[0]||(e[0]=t=>d.searchQuery=t),type:"text",placeholder:"Search...",class:"search-input"},null,512),[[n.nr,d.searchQuery]]),(0,i._)("button",{onClick:e[1]||(e[1]=(...t)=>u.performSearch&&u.performSearch(...t)),class:"search-button"},"SEARCH")])]),d.searchResults.length>0?((0,i.wg)(),(0,i.iD)("div",c,[(0,i._)("ul",null,[((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(d.searchResults,(t=>((0,i.wg)(),(0,i.iD)("li",{key:t.id,class:"search-item"},(0,r.zw)(t.name),1)))),128))])])):((0,i.wg)(),(0,i.iD)("div",p," No results found."+(0,r.zw)(d.text),1))],64)}var u=a(1076),h={data(){return{text:"",searchQuery:"",searchResults:[],allItems:[{id:1,name:"Item 1"},{id:2,name:"Item 2"},{id:3,name:"Item 3"}]}},methods:{test(){u.Z.get("test").then((t=>{this.text=t.data})).catch((t=>{this.text="error"+t}))},performSearch(){this.searchQuery?this.searchResults=this.allItems.filter((t=>t.name.toLowerCase().includes(this.searchQuery.toLowerCase()))):this.searchResults=[]}}},y=a(89);const m=(0,y.Z)(h,[["render",d],["__scopeId","data-v-7dd512a8"]]);var g=m;(0,n.ri)(g).mount("#app")}},e={};function a(n){var i=e[n];if(void 0!==i)return i.exports;var r=e[n]={exports:{}};return t[n].call(r.exports,r,r.exports,a),r.exports}a.m=t,function(){var t=[];a.O=function(e,n,i,r){if(!n){var o=1/0;for(c=0;c<t.length;c++){n=t[c][0],i=t[c][1],r=t[c][2];for(var l=!0,s=0;s<n.length;s++)(!1&r||o>=r)&&Object.keys(a.O).every((function(t){return a.O[t](n[s])}))?n.splice(s--,1):(l=!1,r<o&&(o=r));if(l){t.splice(c--,1);var f=i();void 0!==f&&(e=f)}}return e}r=r||0;for(var c=t.length;c>0&&t[c-1][2]>r;c--)t[c]=t[c-1];t[c]=[n,i,r]}}(),function(){a.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return a.d(e,{a:e}),e}}(),function(){a.d=function(t,e){for(var n in e)a.o(e,n)&&!a.o(t,n)&&Object.defineProperty(t,n,{enumerable:!0,get:e[n]})}}(),function(){a.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"===typeof window)return window}}()}(),function(){a.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),function(){a.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})}}(),function(){a.p="/"}(),function(){var t={143:0};a.O.j=function(e){return 0===t[e]};var e=function(e,n){var i,r,o=n[0],l=n[1],s=n[2],f=0;if(o.some((function(e){return 0!==t[e]}))){for(i in l)a.o(l,i)&&(a.m[i]=l[i]);if(s)var c=s(a)}for(e&&e(n);f<o.length;f++)r=o[f],a.o(t,r)&&t[r]&&t[r][0](),t[r]=0;return a.O(c)},n=self["webpackChunkwebsite"]=self["webpackChunkwebsite"]||[];n.forEach(e.bind(null,0)),n.push=e.bind(null,n.push.bind(n))}();var n=a.O(void 0,[998],(function(){return a(3668)}));n=a.O(n)})();
//# sourceMappingURL=app.981deefc.js.map