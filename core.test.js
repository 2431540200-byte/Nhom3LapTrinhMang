import {test} from 'node:test';
import assert from 'node:assert/strict';
import {matches, validFilter, validateMetrics, roomPrefix, csvCell} from '../assets/core.js';
test('MQTT filters respect level boundaries and reserved topics',()=>{assert(matches('a/+/c','a/b/c'));assert(matches('a/#','a'));assert(!matches('a/+','a'));assert(!matches('#','$SYS/broker'));assert(matches('$SYS/#','$SYS/broker'));});
test('invalid wildcard placements are rejected',()=>{for(const f of ['a/#/b','a/b+','a/##',''])assert(!validFilter(f));assert(validFilter('a/+/b'));});
test('metrics reject nonfinite, strings and out of range values',()=>{assert(validateMetrics({cpu:0,ram:100,disk:45}));for(const cpu of [-1,101,NaN,'4',null])assert(!validateMetrics({cpu,ram:2,disk:3}));});
test('rooms cannot inject MQTT paths',()=>{assert.equal(roomPrefix('ABC123'),'pcmon/v1/ABC123');assert.throws(()=>roomPrefix('a/#'));});
test('CSV escapes quotes and spreadsheet formulas',()=>{assert.equal(csvCell('=1+1'),'"\'=1+1"');assert.equal(csvCell('a"b'),'"a""b"');});
