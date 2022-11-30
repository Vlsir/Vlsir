/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

goog.provide('proto.vlsir.spice.SimResult');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');
goog.require('proto.vlsir.spice.AnalysisResult');


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
proto.vlsir.spice.SimResult = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.vlsir.spice.SimResult.repeatedFields_, null);
};
goog.inherits(proto.vlsir.spice.SimResult, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.vlsir.spice.SimResult.displayName = 'proto.vlsir.spice.SimResult';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.vlsir.spice.SimResult.repeatedFields_ = [1];



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
proto.vlsir.spice.SimResult.prototype.toObject = function(opt_includeInstance) {
  return proto.vlsir.spice.SimResult.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.vlsir.spice.SimResult} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.spice.SimResult.toObject = function(includeInstance, msg) {
  var f, obj = {
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
 * @return {!proto.vlsir.spice.SimResult}
 */
proto.vlsir.spice.SimResult.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.vlsir.spice.SimResult;
  return proto.vlsir.spice.SimResult.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.vlsir.spice.SimResult} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.vlsir.spice.SimResult}
 */
proto.vlsir.spice.SimResult.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
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
proto.vlsir.spice.SimResult.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.vlsir.spice.SimResult.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.vlsir.spice.SimResult} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.spice.SimResult.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getAnList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      1,
      f,
      proto.vlsir.spice.AnalysisResult.serializeBinaryToWriter
    );
  }
};


/**
 * repeated AnalysisResult an = 1;
 * @return {!Array<!proto.vlsir.spice.AnalysisResult>}
 */
proto.vlsir.spice.SimResult.prototype.getAnList = function() {
  return /** @type{!Array<!proto.vlsir.spice.AnalysisResult>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.vlsir.spice.AnalysisResult, 1));
};


/** @param {!Array<!proto.vlsir.spice.AnalysisResult>} value */
proto.vlsir.spice.SimResult.prototype.setAnList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 1, value);
};


/**
 * @param {!proto.vlsir.spice.AnalysisResult=} opt_value
 * @param {number=} opt_index
 * @return {!proto.vlsir.spice.AnalysisResult}
 */
proto.vlsir.spice.SimResult.prototype.addAn = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.vlsir.spice.AnalysisResult, opt_index);
};


proto.vlsir.spice.SimResult.prototype.clearAnList = function() {
  this.setAnList([]);
};


