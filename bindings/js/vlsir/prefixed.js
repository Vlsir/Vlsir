/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

goog.provide('proto.vlsir.utils.Prefixed');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');

goog.forwardDeclare('proto.vlsir.utils.SIPrefix');

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
proto.vlsir.utils.Prefixed = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, proto.vlsir.utils.Prefixed.oneofGroups_);
};
goog.inherits(proto.vlsir.utils.Prefixed, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.vlsir.utils.Prefixed.displayName = 'proto.vlsir.utils.Prefixed';
}
/**
 * Oneof group definitions for this message. Each group defines the field
 * numbers belonging to that group. When of these fields' value is set, all
 * other fields in the group are cleared. During deserialization, if multiple
 * fields are encountered for a group, only the last value seen will be kept.
 * @private {!Array<!Array<number>>}
 * @const
 */
proto.vlsir.utils.Prefixed.oneofGroups_ = [[2,3,4]];

/**
 * @enum {number}
 */
proto.vlsir.utils.Prefixed.NumberCase = {
  NUMBER_NOT_SET: 0,
  INTEGER: 2,
  DOUBLE: 3,
  STRING: 4
};

/**
 * @return {proto.vlsir.utils.Prefixed.NumberCase}
 */
proto.vlsir.utils.Prefixed.prototype.getNumberCase = function() {
  return /** @type {proto.vlsir.utils.Prefixed.NumberCase} */(jspb.Message.computeOneofCase(this, proto.vlsir.utils.Prefixed.oneofGroups_[0]));
};



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
proto.vlsir.utils.Prefixed.prototype.toObject = function(opt_includeInstance) {
  return proto.vlsir.utils.Prefixed.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.vlsir.utils.Prefixed} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.utils.Prefixed.toObject = function(includeInstance, msg) {
  var f, obj = {
    prefix: jspb.Message.getFieldWithDefault(msg, 1, 0),
    integer: jspb.Message.getFieldWithDefault(msg, 2, 0),
    pb_double: +jspb.Message.getFieldWithDefault(msg, 3, 0.0),
    string: jspb.Message.getFieldWithDefault(msg, 4, "")
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
 * @return {!proto.vlsir.utils.Prefixed}
 */
proto.vlsir.utils.Prefixed.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.vlsir.utils.Prefixed;
  return proto.vlsir.utils.Prefixed.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.vlsir.utils.Prefixed} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.vlsir.utils.Prefixed}
 */
proto.vlsir.utils.Prefixed.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {!proto.vlsir.utils.SIPrefix} */ (reader.readEnum());
      msg.setPrefix(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt64());
      msg.setInteger(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readDouble());
      msg.setDouble(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setString(value);
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
proto.vlsir.utils.Prefixed.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.vlsir.utils.Prefixed.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.vlsir.utils.Prefixed} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.utils.Prefixed.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getPrefix();
  if (f !== 0.0) {
    writer.writeEnum(
      1,
      f
    );
  }
  f = /** @type {number} */ (jspb.Message.getField(message, 2));
  if (f != null) {
    writer.writeInt64(
      2,
      f
    );
  }
  f = /** @type {number} */ (jspb.Message.getField(message, 3));
  if (f != null) {
    writer.writeDouble(
      3,
      f
    );
  }
  f = /** @type {string} */ (jspb.Message.getField(message, 4));
  if (f != null) {
    writer.writeString(
      4,
      f
    );
  }
};


/**
 * optional SIPrefix prefix = 1;
 * @return {!proto.vlsir.utils.SIPrefix}
 */
proto.vlsir.utils.Prefixed.prototype.getPrefix = function() {
  return /** @type {!proto.vlsir.utils.SIPrefix} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/** @param {!proto.vlsir.utils.SIPrefix} value */
proto.vlsir.utils.Prefixed.prototype.setPrefix = function(value) {
  jspb.Message.setProto3EnumField(this, 1, value);
};


/**
 * optional int64 integer = 2;
 * @return {number}
 */
proto.vlsir.utils.Prefixed.prototype.getInteger = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/** @param {number} value */
proto.vlsir.utils.Prefixed.prototype.setInteger = function(value) {
  jspb.Message.setOneofField(this, 2, proto.vlsir.utils.Prefixed.oneofGroups_[0], value);
};


proto.vlsir.utils.Prefixed.prototype.clearInteger = function() {
  jspb.Message.setOneofField(this, 2, proto.vlsir.utils.Prefixed.oneofGroups_[0], undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.vlsir.utils.Prefixed.prototype.hasInteger = function() {
  return jspb.Message.getField(this, 2) != null;
};


/**
 * optional double double = 3;
 * @return {number}
 */
proto.vlsir.utils.Prefixed.prototype.getDouble = function() {
  return /** @type {number} */ (+jspb.Message.getFieldWithDefault(this, 3, 0.0));
};


/** @param {number} value */
proto.vlsir.utils.Prefixed.prototype.setDouble = function(value) {
  jspb.Message.setOneofField(this, 3, proto.vlsir.utils.Prefixed.oneofGroups_[0], value);
};


proto.vlsir.utils.Prefixed.prototype.clearDouble = function() {
  jspb.Message.setOneofField(this, 3, proto.vlsir.utils.Prefixed.oneofGroups_[0], undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.vlsir.utils.Prefixed.prototype.hasDouble = function() {
  return jspb.Message.getField(this, 3) != null;
};


/**
 * optional string string = 4;
 * @return {string}
 */
proto.vlsir.utils.Prefixed.prototype.getString = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/** @param {string} value */
proto.vlsir.utils.Prefixed.prototype.setString = function(value) {
  jspb.Message.setOneofField(this, 4, proto.vlsir.utils.Prefixed.oneofGroups_[0], value);
};


proto.vlsir.utils.Prefixed.prototype.clearString = function() {
  jspb.Message.setOneofField(this, 4, proto.vlsir.utils.Prefixed.oneofGroups_[0], undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.vlsir.utils.Prefixed.prototype.hasString = function() {
  return jspb.Message.getField(this, 4) != null;
};


