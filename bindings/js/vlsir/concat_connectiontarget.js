// source: circuit.proto
/**
 * @fileoverview
 * @enhanceable
 * @suppress {missingRequire} reports error on implicit type usages.
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!
/* eslint-disable */
// @ts-nocheck

goog.provide('proto.vlsir.circuit.Concat');
goog.provide('proto.vlsir.circuit.ConnectionTarget');
goog.provide('proto.vlsir.circuit.ConnectionTarget.StypeCase');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');
goog.require('proto.vlsir.circuit.Slice');

/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.vlsir.circuit.Concat = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.vlsir.circuit.Concat.repeatedFields_, null);
};
goog.inherits(proto.vlsir.circuit.Concat, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.vlsir.circuit.Concat.displayName = 'proto.vlsir.circuit.Concat';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.vlsir.circuit.ConnectionTarget = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, proto.vlsir.circuit.ConnectionTarget.oneofGroups_);
};
goog.inherits(proto.vlsir.circuit.ConnectionTarget, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.vlsir.circuit.ConnectionTarget.displayName = 'proto.vlsir.circuit.ConnectionTarget';
}

/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.vlsir.circuit.Concat.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.vlsir.circuit.Concat.prototype.toObject = function(opt_includeInstance) {
  return proto.vlsir.circuit.Concat.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.vlsir.circuit.Concat} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.circuit.Concat.toObject = function(includeInstance, msg) {
  var f, obj = {
    partsList: jspb.Message.toObjectList(msg.getPartsList(),
    proto.vlsir.circuit.ConnectionTarget.toObject, includeInstance)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.vlsir.circuit.Concat}
 */
proto.vlsir.circuit.Concat.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.vlsir.circuit.Concat;
  return proto.vlsir.circuit.Concat.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.vlsir.circuit.Concat} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.vlsir.circuit.Concat}
 */
proto.vlsir.circuit.Concat.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.vlsir.circuit.ConnectionTarget;
      reader.readMessage(value,proto.vlsir.circuit.ConnectionTarget.deserializeBinaryFromReader);
      msg.addParts(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.vlsir.circuit.Concat.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.vlsir.circuit.Concat.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.vlsir.circuit.Concat} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.circuit.Concat.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getPartsList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      1,
      f,
      proto.vlsir.circuit.ConnectionTarget.serializeBinaryToWriter
    );
  }
};


/**
 * repeated ConnectionTarget parts = 1;
 * @return {!Array<!proto.vlsir.circuit.ConnectionTarget>}
 */
proto.vlsir.circuit.Concat.prototype.getPartsList = function() {
  return /** @type{!Array<!proto.vlsir.circuit.ConnectionTarget>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.vlsir.circuit.ConnectionTarget, 1));
};


/**
 * @param {!Array<!proto.vlsir.circuit.ConnectionTarget>} value
 * @return {!proto.vlsir.circuit.Concat} returns this
*/
proto.vlsir.circuit.Concat.prototype.setPartsList = function(value) {
  return jspb.Message.setRepeatedWrapperField(this, 1, value);
};


/**
 * @param {!proto.vlsir.circuit.ConnectionTarget=} opt_value
 * @param {number=} opt_index
 * @return {!proto.vlsir.circuit.ConnectionTarget}
 */
proto.vlsir.circuit.Concat.prototype.addParts = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.vlsir.circuit.ConnectionTarget, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.vlsir.circuit.Concat} returns this
 */
proto.vlsir.circuit.Concat.prototype.clearPartsList = function() {
  return this.setPartsList([]);
};



/**
 * Oneof group definitions for this message. Each group defines the field
 * numbers belonging to that group. When of these fields' value is set, all
 * other fields in the group are cleared. During deserialization, if multiple
 * fields are encountered for a group, only the last value seen will be kept.
 * @private {!Array<!Array<number>>}
 * @const
 */
proto.vlsir.circuit.ConnectionTarget.oneofGroups_ = [[1,2,3]];

/**
 * @enum {number}
 */
proto.vlsir.circuit.ConnectionTarget.StypeCase = {
  STYPE_NOT_SET: 0,
  SIG: 1,
  SLICE: 2,
  CONCAT: 3
};

/**
 * @return {proto.vlsir.circuit.ConnectionTarget.StypeCase}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.getStypeCase = function() {
  return /** @type {proto.vlsir.circuit.ConnectionTarget.StypeCase} */(jspb.Message.computeOneofCase(this, proto.vlsir.circuit.ConnectionTarget.oneofGroups_[0]));
};



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.toObject = function(opt_includeInstance) {
  return proto.vlsir.circuit.ConnectionTarget.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.vlsir.circuit.ConnectionTarget} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.circuit.ConnectionTarget.toObject = function(includeInstance, msg) {
  var f, obj = {
    sig: jspb.Message.getFieldWithDefault(msg, 1, ""),
    slice: (f = msg.getSlice()) && proto.vlsir.circuit.Slice.toObject(includeInstance, f),
    concat: (f = msg.getConcat()) && proto.vlsir.circuit.Concat.toObject(includeInstance, f)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.vlsir.circuit.ConnectionTarget}
 */
proto.vlsir.circuit.ConnectionTarget.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.vlsir.circuit.ConnectionTarget;
  return proto.vlsir.circuit.ConnectionTarget.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.vlsir.circuit.ConnectionTarget} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.vlsir.circuit.ConnectionTarget}
 */
proto.vlsir.circuit.ConnectionTarget.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSig(value);
      break;
    case 2:
      var value = new proto.vlsir.circuit.Slice;
      reader.readMessage(value,proto.vlsir.circuit.Slice.deserializeBinaryFromReader);
      msg.setSlice(value);
      break;
    case 3:
      var value = new proto.vlsir.circuit.Concat;
      reader.readMessage(value,proto.vlsir.circuit.Concat.deserializeBinaryFromReader);
      msg.setConcat(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.vlsir.circuit.ConnectionTarget.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.vlsir.circuit.ConnectionTarget} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.circuit.ConnectionTarget.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = /** @type {string} */ (jspb.Message.getField(message, 1));
  if (f != null) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getSlice();
  if (f != null) {
    writer.writeMessage(
      2,
      f,
      proto.vlsir.circuit.Slice.serializeBinaryToWriter
    );
  }
  f = message.getConcat();
  if (f != null) {
    writer.writeMessage(
      3,
      f,
      proto.vlsir.circuit.Concat.serializeBinaryToWriter
    );
  }
};


/**
 * optional string sig = 1;
 * @return {string}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.getSig = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.vlsir.circuit.ConnectionTarget} returns this
 */
proto.vlsir.circuit.ConnectionTarget.prototype.setSig = function(value) {
  return jspb.Message.setOneofField(this, 1, proto.vlsir.circuit.ConnectionTarget.oneofGroups_[0], value);
};


/**
 * Clears the field making it undefined.
 * @return {!proto.vlsir.circuit.ConnectionTarget} returns this
 */
proto.vlsir.circuit.ConnectionTarget.prototype.clearSig = function() {
  return jspb.Message.setOneofField(this, 1, proto.vlsir.circuit.ConnectionTarget.oneofGroups_[0], undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.hasSig = function() {
  return jspb.Message.getField(this, 1) != null;
};


/**
 * optional Slice slice = 2;
 * @return {?proto.vlsir.circuit.Slice}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.getSlice = function() {
  return /** @type{?proto.vlsir.circuit.Slice} */ (
    jspb.Message.getWrapperField(this, proto.vlsir.circuit.Slice, 2));
};


/**
 * @param {?proto.vlsir.circuit.Slice|undefined} value
 * @return {!proto.vlsir.circuit.ConnectionTarget} returns this
*/
proto.vlsir.circuit.ConnectionTarget.prototype.setSlice = function(value) {
  return jspb.Message.setOneofWrapperField(this, 2, proto.vlsir.circuit.ConnectionTarget.oneofGroups_[0], value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.vlsir.circuit.ConnectionTarget} returns this
 */
proto.vlsir.circuit.ConnectionTarget.prototype.clearSlice = function() {
  return this.setSlice(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.hasSlice = function() {
  return jspb.Message.getField(this, 2) != null;
};


/**
 * optional Concat concat = 3;
 * @return {?proto.vlsir.circuit.Concat}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.getConcat = function() {
  return /** @type{?proto.vlsir.circuit.Concat} */ (
    jspb.Message.getWrapperField(this, proto.vlsir.circuit.Concat, 3));
};


/**
 * @param {?proto.vlsir.circuit.Concat|undefined} value
 * @return {!proto.vlsir.circuit.ConnectionTarget} returns this
*/
proto.vlsir.circuit.ConnectionTarget.prototype.setConcat = function(value) {
  return jspb.Message.setOneofWrapperField(this, 3, proto.vlsir.circuit.ConnectionTarget.oneofGroups_[0], value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.vlsir.circuit.ConnectionTarget} returns this
 */
proto.vlsir.circuit.ConnectionTarget.prototype.clearConcat = function() {
  return this.setConcat(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.circuit.ConnectionTarget.prototype.hasConcat = function() {
  return jspb.Message.getField(this, 3) != null;
};


