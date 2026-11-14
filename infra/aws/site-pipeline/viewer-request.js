// CloudFront Function (viewer-request), vasl-marketing-viewer-request,
// distribution E11DM7B5W2KRCQ. gotovasl.com, November 2026.
//
// 1. Retired pages return 301 to their nearest new page. The map is generated
//    from tools/retired.py; tools/retire_pages.py --check fails if they drift.
// 2. Pretty URLs: S3 stores pages flat as <page>.html, so /about serves
//    about.html and / serves index.html. A path with a dot is served as is.
//
// Applied through Terraform with the rest of the distribution. Until it is,
// every retired file is also a noindex refresh stub, so old links still land.
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

function handler(event) {
  var req = event.request;
  var uri = req.uri;
  if (uri.length > 1) uri = uri.replace(/\/+$/, '');
  var key = uri.replace(/\.html$/, '');

  if (RETIRED[key] !== undefined) {
    return {
      statusCode: 301,
      statusDescription: 'Moved Permanently',
      headers: { location: { value: 'https://gotovasl.com' + RETIRED[key] } }
    };
  }

  if (uri === '/' || uri === '') {
    req.uri = '/index.html';
  } else if (uri.split('/').pop().indexOf('.') === -1) {
    req.uri = uri + '.html';
  } else {
    req.uri = uri;
  }
  return req;
}
