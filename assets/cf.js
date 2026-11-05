/* Loads Cloudflare Web Analytics unless this browser opted out (visit any page with ?nocount once; ?count turns it back on). */
(function () {
  try {
    var q = location.search;
    if (q.indexOf("nocount") > -1) localStorage.setItem("lumi-nocount", "1");
    if (q.indexOf("count=on") > -1) localStorage.removeItem("lumi-nocount");
    if (localStorage.getItem("lumi-nocount")) { document.documentElement.dataset.nocount = "1"; return; }
  } catch (e) {}
  var s = document.createElement("script");
  s.src = "https://static.cloudflareinsights.com/beacon.min.js";
  s.setAttribute("data-cf-beacon", '{"token": "4f74bf30d2654aa48943d2ab2bf50fdf"}');
  s.defer = true;
  document.head.appendChild(s);
})();
