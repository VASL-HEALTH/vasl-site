// CloudFront Function (viewer-request), vasl-marketing-viewer-request,
// distribution E11DM7B5W2KRCQ. gotovasl.com, November 2026.
//
// MERGED 2026-11-14: the November rebuild's rules plus the two host/path
// canonicalizations the previous live function carried. Dropping either was a
// silent regression on a live site, so they are back and tested.
//
// RULE ORDER, AND IT MATTERS:
//   1. www.gotovasl.com -> https://gotovasl.com, path and query preserved.
//      The distribution serves BOTH hostnames as aliases, so without this the
//      same page answers on two hosts and neither is canonical.
//   2. Trailing slash -> the no-slash form. /about/ and /about are two URLs for
//      one document; S3 stores pages flat, so <dir>/index.html exists only at
//      the root and every /about/ style URL 404'd before this rule existed.
//      Search Console had reported those as "Not found (404)".
//   3. Retired pages -> 301 to their nearest replacement, query preserved.
//   4. Pretty URLs -> <page>.html; a path whose last segment has a dot is
//      served as-is.
//
// The slash is normalized INSIDE the www redirect rather than after it, so a
// request wrong on both counts (www.gotovasl.com/about/) costs exactly ONE
// 301 instead of two. Running them in sequence sent www/about/ -> apex/about/
// -> apex/about, which is a measurable extra round trip on every such link.
//
// /demo IS DELIBERATELY NOT REDIRECTED. The previous function sent it to
// demo.gotovasl.com, which is NXDOMAIN -- a 301 to nowhere. site/demo.html
// exists and forwards to the VLAP demo, so the pretty-URL rewrite below
// resolves /demo to that page. Ruled 2026-11-14.
//
// The retired map is generated from tools/retired.py; tools/retire_pages.py
// --check fails if they drift.
//
// TWO COPIES, KEPT IDENTICAL. The function is Terraform-managed in
// VASL-PLATFORM infra/aws/static-sites/functions/viewer-request.js. This file
// is the source of record for the site repo; they must match byte for byte.
var RETIRED = {
  '/for-schools': '/',
  '/for-organizations': '/',
  '/for-families': '/',
  '/school-mental-health-rfp': '/',
  '/platform': '/',
  '/peer-groups': '/',
  '/ai-model': '/vlap',
  '/glossary': '/vlap',
  '/teletherapy': '/vlap',
  '/outcomes': '/research',
  '/clinical-outcomes': '/research',
  '/dialect-bias-mental-health-screening': '/research',
  '/hedis-behavioral-health-cultural-fit': '/bridge',
  '/infrastructure': '/technology',
  '/careers': '/team',
  '/support': '/contact',
  '/help/assessments': '/technology',
  '/help/billing': '/technology',
  '/help/clinical': '/technology',
  '/help/compliance': '/technology',
  '/help/getting-started': '/technology',
  '/help/technical': '/technology',
  '/help/vlap-technology': '/vlap'
};

// Carry the query string across a redirect, so /support?subject=Pricing keeps
// its subject when it lands on /contact. A viewer-request function gets the
// parsed object and no raw string, so it is rebuilt here. Valueless keys
// (?foo) must stay bare rather than becoming "foo=".
function qs(q) {
  var parts = [];
  for (var k in q) {
    if (q[k].multiValue) {
      for (var i = 0; i < q[k].multiValue.length; i++) {
        var mv = q[k].multiValue[i].value;
        parts.push(mv ? k + '=' + mv : k);
      }
    } else {
      parts.push(q[k].value ? k + '=' + q[k].value : k);
    }
  }
  return parts.length ? '?' + parts.join('&') : '';
}

function redirect(location) {
  return {
    statusCode: 301,
    statusDescription: 'Moved Permanently',
    headers: { location: { value: location } }
  };
}

function handler(event) {
  var req = event.request;
  var host = req.headers.host ? req.headers.host.value : '';
  var uri = req.uri;

  // The canonical path: no trailing slash, except "/" itself, which is the
  // homepage rather than a slash variant. A path of only slashes collapses
  // back to it.
  var path = uri;
  if (path.length > 1) {
    path = path.replace(/\/+$/, '') || '/';
  }

  // 1. www -> apex, first, carrying the canonical path so a www request with a
  //    trailing slash is fixed in this single hop.
  if (host === 'www.gotovasl.com') {
    return redirect('https://gotovasl.com' + path + qs(req.querystring));
  }

  // 2. Trailing slash on the apex -> the canonical no-slash URL.
  if (path !== uri) {
    return redirect('https://gotovasl.com' + path + qs(req.querystring));
  }

  // 3. Retired pages. Keyed on the extensionless form so /platform and
  //    /platform.html both redirect.
  var key = path.replace(/\.html$/, '');
  if (RETIRED[key] !== undefined) {
    return redirect('https://gotovasl.com' + RETIRED[key] + qs(req.querystring));
  }

  // 4. Pretty URLs. Only the last segment is checked for a dot, so a dotted
  //    directory (/v1.2/page) is not mistaken for a file.
  if (path === '/' || path === '') {
    req.uri = '/index.html';
  } else if (path.split('/').pop().indexOf('.') === -1) {
    req.uri = path + '.html';
  } else {
    req.uri = path;
  }

  return req;
}
