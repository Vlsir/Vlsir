/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

goog.provide('proto.vlsir.spice.SweepResult');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');
goog.require('proto.vlsir.spice.AnalysisResult');
goog.require('proto.vlsir.spice.Sweep');


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
proto.vlsir.spice.SweepResult = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.vlsir.spice.SweepResult.repeatedFields_, null);
};
goog.inherits(proto.vlsir.spice.SweepResult, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.vlsir.spice.SweepResult.displayName = 'proto.vlsir.spice.SweepResult';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.vlsir.spice.SweepResult.repeatedFields_ = [4];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.vlsir.spice.SweepResult.prototype.toObject = function(opt_includeInstance) {
  return proto.vlsir.spice.SweepResult.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.vlsir.spice.SweepResult} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.spice.SweepResult.toObject = function(includeInstance, msg) {
  var f, obj = {
    analysisName: jspb.Message.getFieldWithDefault(msg, 1, ""),
    variable: jspb.Message.getFieldWithDefault(msg, 2, ""),
    sweep: (f = msg.getSweep()) && proto.vlsir.spice.Sweep.toObject(includeInstance, f),
    anList: jspb.Message.toObjectList(msg.getAnList(),
    proto.vlsir.spice.AnalysisResult.toObject, includeInstance)
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
 * @return {!proto.vlsir.spice.SweepResult}
 */
proto.vlsir.spice.SweepResult.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.vlsir.spice.SweepResult;
  return proto.vlsir.spice.SweepResult.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.vlsir.spice.SweepResult} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.vlsir.spice.SweepResult}
 */
proto.vlsir.spice.SweepResult.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setAnalysisName(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setVariable(value);
      break;
    case 3:
      var value = new proto.vlsir.spice.Sweep;
      reader.readMessage(value,proto.vlsir.spice.Sweep.deserializeBinaryFromReader);
      msg.setSweep(value);
      break;
    case 4:
      var value = new proto.vlsir.spice.AnalysisResult;
      reader.readMessage(value,proto.vlsir.spice.AnalysisResult.deserializeBinaryFromReader);
      msg.addAn(value);
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
proto.vlsir.spice.SweepResult.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.vlsir.spice.SweepResult.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.vlsir.spice.SweepResult} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.spice.SweepResult.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getAnalysisName();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getVariable();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getSweep();
  if (f != null) {
    writer.writeMessage(
      3,
      f,
      proto.vlsir.spice.Sweep.serializeBinaryToWriter
    );
  }
  f = message.getAnList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      4,
      f,
      proto.vlsir.spice.AnalysisResult.serializeBinaryToWriter
    );
  }
};


/**
 * optional string analysis_name = 1;
 * @return {string}
 */
proto.vlsir.spice.SweepResult.prototype.getAnalysisName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.vlsir.spice.SweepResult.prototype.setAnalysisName = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string variable = 2;
 * @return {string}
 */
proto.vlsir.spice.SweepResult.prototype.getVariable = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/** @param {string} value */
proto.vlsir.spice.SweepResult.prototype.setVariable = function(value) {
  jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional Sweep sweep = 3;
 * @return {?proto.vlsir.spice.Sweep}
 */
proto.vlsir.spice.SweepResult.prototype.getSweep = function() {
  return /** @type{?proto.vlsir.spice.Sweep} */ (
    jspb.Message.getWrapperField(this, proto.vlsir.spice.Sweep, 3));
};


/** @param {?proto.vlsir.spice.Sweep|undefined} value */
proto.vlsir.spice.SweepResult.prototype.setSweep = function(value) {
  jspb.Message.setWrapperField(this, 3, value);
};


proto.vlsir.spice.SweepResult.prototype.clearSweep = function() {
  this.setSweep(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.vlsir.spice.SweepResult.prototype.hasSweep = function() {
  return jspb.Message.getField(this, 3) != null;
};


/**
 * repeated AnalysisResult an = 4;
 * @return {!Array<!proto.vlsir.spice.AnalysisResult>}
 */
proto.vlsir.spice.SweepResult.prototype.getAnList = function() {
  return /** @type{!Array<!proto.vlsir.spice.AnalysisResult>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.vlsir.spice.AnalysisResult, 4));
};


/** @param {!Array<!proto.vlsir.spice.AnalysisResult>} value */
proto.vlsir.spice.SweepResult.prototype.setAnList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 4, value);
};


/**
 * @param {!proto.vlsir.spice.AnalysisResult=} opt_value
 * @param {number=} opt_index
 * @return {!proto.vlsir.spice.AnalysisResult}
 */
proto.vlsir.spice.SweepResult.prototype.addAn = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 4, opt_value, proto.vlsir.spice.AnalysisResult, opt_index);
};


proto.vlsir.spice.SweepResult.prototype.clearAnList = function() {
  this.setAnList([]);
};


