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

goog.provide('proto.vlsir.circuit.Instance');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');
goog.require('proto.vlsir.circuit.Connection');
goog.require('proto.vlsir.utils.Param');
goog.require('proto.vlsir.utils.Reference');

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
proto.vlsir.circuit.Instance = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.vlsir.circuit.Instance.repeatedFields_, null);
};
goog.inherits(proto.vlsir.circuit.Instance, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.vlsir.circuit.Instance.displayName = 'proto.vlsir.circuit.Instance';
}

/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.vlsir.circuit.Instance.repeatedFields_ = [3,4];



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
proto.vlsir.circuit.Instance.prototype.toObject = function(opt_includeInstance) {
  return proto.vlsir.circuit.Instance.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.vlsir.circuit.Instance} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.circuit.Instance.toObject = function(includeInstance, msg) {
  var f, obj = {
    name: jspb.Message.getFieldWithDefault(msg, 1, ""),
    module: (f = msg.getModule()) && proto.vlsir.utils.Reference.toObject(includeInstance, f),
    parametersList: jspb.Message.toObjectList(msg.getParametersList(),
    proto.vlsir.utils.Param.toObject, includeInstance),
    connectionsList: jspb.Message.toObjectList(msg.getConnectionsList(),
    proto.vlsir.circuit.Connection.toObject, includeInstance)
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
 * @return {!proto.vlsir.circuit.Instance}
 */
proto.vlsir.circuit.Instance.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.vlsir.circuit.Instance;
  return proto.vlsir.circuit.Instance.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.vlsir.circuit.Instance} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.vlsir.circuit.Instance}
 */
proto.vlsir.circuit.Instance.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setName(value);
      break;
    case 2:
      var value = new proto.vlsir.utils.Reference;
      reader.readMessage(value,proto.vlsir.utils.Reference.deserializeBinaryFromReader);
      msg.setModule(value);
      break;
    case 3:
      var value = new proto.vlsir.utils.Param;
      reader.readMessage(value,proto.vlsir.utils.Param.deserializeBinaryFromReader);
      msg.addParameters(value);
      break;
    case 4:
      var value = new proto.vlsir.circuit.Connection;
      reader.readMessage(value,proto.vlsir.circuit.Connection.deserializeBinaryFromReader);
      msg.addConnections(value);
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
proto.vlsir.circuit.Instance.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.vlsir.circuit.Instance.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.vlsir.circuit.Instance} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.circuit.Instance.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getName();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getModule();
  if (f != null) {
    writer.writeMessage(
      2,
      f,
      proto.vlsir.utils.Reference.serializeBinaryToWriter
    );
  }
  f = message.getParametersList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      3,
      f,
      proto.vlsir.utils.Param.serializeBinaryToWriter
    );
  }
  f = message.getConnectionsList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      4,
      f,
      proto.vlsir.circuit.Connection.serializeBinaryToWriter
    );
  }
};


/**
 * optional string name = 1;
 * @return {string}
 */
proto.vlsir.circuit.Instance.prototype.getName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.vlsir.circuit.Instance} returns this
 */
proto.vlsir.circuit.Instance.prototype.setName = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional vlsir.utils.Reference module = 2;
 * @return {?proto.vlsir.utils.Reference}
 */
proto.vlsir.circuit.Instance.prototype.getModule = function() {
  return /** @type{?proto.vlsir.utils.Reference} */ (
    jspb.Message.getWrapperField(this, proto.vlsir.utils.Reference, 2));
};


/**
 * @param {?proto.vlsir.utils.Reference|undefined} value
 * @return {!proto.vlsir.circuit.Instance} returns this
*/
proto.vlsir.circuit.Instance.prototype.setModule = function(value) {
  return jspb.Message.setWrapperField(this, 2, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.vlsir.circuit.Instance} returns this
 */
proto.vlsir.circuit.Instance.prototype.clearModule = function() {
  return this.setModule(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.circuit.Instance.prototype.hasModule = function() {
  return jspb.Message.getField(this, 2) != null;
};


/**
 * repeated vlsir.utils.Param parameters = 3;
 * @return {!Array<!proto.vlsir.utils.Param>}
 */
proto.vlsir.circuit.Instance.prototype.getParametersList = function() {
  return /** @type{!Array<!proto.vlsir.utils.Param>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.vlsir.utils.Param, 3));
};


/**
 * @param {!Array<!proto.vlsir.utils.Param>} value
 * @return {!proto.vlsir.circuit.Instance} returns this
*/
proto.vlsir.circuit.Instance.prototype.setParametersList = function(value) {
  return jspb.Message.setRepeatedWrapperField(this, 3, value);
};


/**
 * @param {!proto.vlsir.utils.Param=} opt_value
 * @param {number=} opt_index
 * @return {!proto.vlsir.utils.Param}
 */
proto.vlsir.circuit.Instance.prototype.addParameters = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 3, opt_value, proto.vlsir.utils.Param, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.vlsir.circuit.Instance} returns this
 */
proto.vlsir.circuit.Instance.prototype.clearParametersList = function() {
  return this.setParametersList([]);
};


/**
 * repeated Connection connections = 4;
 * @return {!Array<!proto.vlsir.circuit.Connection>}
 */
proto.vlsir.circuit.Instance.prototype.getConnectionsList = function() {
  return /** @type{!Array<!proto.vlsir.circuit.Connection>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.vlsir.circuit.Connection, 4));
};


/**
 * @param {!Array<!proto.vlsir.circuit.Connection>} value
 * @return {!proto.vlsir.circuit.Instance} returns this
*/
proto.vlsir.circuit.Instance.prototype.setConnectionsList = function(value) {
  return jspb.Message.setRepeatedWrapperField(this, 4, value);
};


/**
 * @param {!proto.vlsir.circuit.Connection=} opt_value
 * @param {number=} opt_index
 * @return {!proto.vlsir.circuit.Connection}
 */
proto.vlsir.circuit.Instance.prototype.addConnections = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 4, opt_value, proto.vlsir.circuit.Connection, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.vlsir.circuit.Instance} returns this
 */
proto.vlsir.circuit.Instance.prototype.clearConnectionsList = function() {
  return this.setConnectionsList([]);
};


