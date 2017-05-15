'use strict';

angular.module('doraFrontend.version', [
  'doraFrontend.version.interpolate-filter',
  'doraFrontend.version.version-directive'
])

.value('version', '0.1');
