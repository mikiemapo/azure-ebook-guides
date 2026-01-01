(function() {
  var prodWorkerUrl = 'https://az104-study-api.azure-hub.workers.dev';
  var githubPagesHost = 'mikiemapo.github.io';
  
  var isProduction = window.location.hostname === githubPagesHost || 
                     window.location.hostname.endsWith('.github.io');
  
  window.AZ104_API_CONFIG = {
    baseUrl: isProduction ? prodWorkerUrl : ''
  };
})();
