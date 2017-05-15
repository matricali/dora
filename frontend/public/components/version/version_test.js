'use strict';

describe('doraFrontend.version module', function() {
  beforeEach(module('doraFrontend.version'));

  describe('version service', function() {
    it('should return current version', inject(function(version) {
      expect(version).toEqual('0.1');
    }));
  });
});
