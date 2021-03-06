// source: utils.proto
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

goog.provide('proto.vlsir.utils.ParamValue');
goog.provide('proto.vlsir.utils.ParamValue.ValueCase');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');
goog.require('proto.vlsir.utils.Prefixed');

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
proto.vlsir.utils.ParamValue = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, proto.vlsir.utils.ParamValue.oneofGroups_);
};
goog.inherits(proto.vlsir.utils.ParamValue, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.vlsir.utils.ParamValue.displayName = 'proto.vlsir.utils.ParamValue';
}

/**
 * Oneof group definitions for this message. Each group defines the field
 * numbers belonging to that group. When of these fields' value is set, all
 * other fields in the group are cleared. During deserialization, if multiple
 * fields are encountered for a group, only the last value seen will be kept.
 * @private {!Array<!Array<number>>}
 * @const
 */
proto.vlsir.utils.ParamValue.oneofGroups_ = [[2,3,4,5,6]];

/**
 * @enum {number}
 */
proto.vlsir.utils.ParamValue.ValueCase = {
  VALUE_NOT_SET: 0,
  INTEGER: 2,
  DOUBLE: 3,
  STRING: 4,
  LITERAL: 5,
  PREFIXED: 6
};

/**
 * @return {proto.vlsir.utils.ParamValue.ValueCase}
 */
proto.vlsir.utils.ParamValue.prototype.getValueCase = function() {
  return /** @type {proto.vlsir.utils.ParamValue.ValueCase} */(jspb.Message.computeOneofCase(this, proto.vlsir.utils.ParamValue.oneofGroups_[0]));
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
proto.vlsir.utils.ParamValue.prototype.toObject = function(opt_includeInstance) {
  return proto.vlsir.utils.ParamValue.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.vlsir.utils.ParamValue} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.utils.ParamValue.toObject = function(includeInstance, msg) {
  var f, obj = {
    integer: jspb.Message.getFieldWithDefault(msg, 2, 0),
    pb_double: jspb.Message.getFloatingPointFieldWithDefault(msg, 3, 0.0),
    string: jspb.Message.getFieldWithDefault(msg, 4, ""),
    literal: jspb.Message.getFieldWithDefault(msg, 5, ""),
    prefixed: (f = msg.getPrefixed()) && proto.vlsir.utils.Prefixed.toObject(includeInstance, f)
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
 * @return {!proto.vlsir.utils.ParamValue}
 */
proto.vlsir.utils.ParamValue.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.vlsir.utils.ParamValue;
  return proto.vlsir.utils.ParamValue.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.vlsir.utils.ParamValue} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.vlsir.utils.ParamValue}
 */
proto.vlsir.utils.ParamValue.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
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
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setLiteral(value);
      break;
    case 6:
      var value = new proto.vlsir.utils.Prefixed;
      reader.readMessage(value,proto.vlsir.utils.Prefixed.deserializeBinaryFromReader);
      msg.setPrefixed(value);
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
proto.vlsir.utils.ParamValue.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.vlsir.utils.ParamValue.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.vlsir.utils.ParamValue} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.utils.ParamValue.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
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
  f = /** @type {string} */ (jspb.Message.getField(message, 5));
  if (f != null) {
    writer.writeString(
      5,
      f
    );
  }
  f = message.getPrefixed();
  if (f != null) {
    writer.writeMessage(
      6,
      f,
      proto.vlsir.utils.Prefixed.serializeBinaryToWriter
    );
  }
};


/**
 * optional int64 integer = 2;
 * @return {number}
 */
proto.vlsir.utils.ParamValue.prototype.getInteger = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.setInteger = function(value) {
  return jspb.Message.setOneofField(this, 2, proto.vlsir.utils.ParamValue.oneofGroups_[0], value);
};


/**
 * Clears the field making it undefined.
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.clearInteger = function() {
  return jspb.Message.setOneofField(this, 2, proto.vlsir.utils.ParamValue.oneofGroups_[0], undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.utils.ParamValue.prototype.hasInteger = function() {
  return jspb.Message.getField(this, 2) != null;
};


/**
 * optional double double = 3;
 * @return {number}
 */
proto.vlsir.utils.ParamValue.prototype.getDouble = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 3, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.setDouble = function(value) {
  return jspb.Message.setOneofField(this, 3, proto.vlsir.utils.ParamValue.oneofGroups_[0], value);
};


/**
 * Clears the field making it undefined.
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.clearDouble = function() {
  return jspb.Message.setOneofField(this, 3, proto.vlsir.utils.ParamValue.oneofGroups_[0], undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.utils.ParamValue.prototype.hasDouble = function() {
  return jspb.Message.getField(this, 3) != null;
};


/**
 * optional string string = 4;
 * @return {string}
 */
proto.vlsir.utils.ParamValue.prototype.getString = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.setString = function(value) {
  return jspb.Message.setOneofField(this, 4, proto.vlsir.utils.ParamValue.oneofGroups_[0], value);
};


/**
 * Clears the field making it undefined.
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.clearString = function() {
  return jspb.Message.setOneofField(this, 4, proto.vlsir.utils.ParamValue.oneofGroups_[0], undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.utils.ParamValue.prototype.hasString = function() {
  return jspb.Message.getField(this, 4) != null;
};


/**
 * optional string literal = 5;
 * @return {string}
 */
proto.vlsir.utils.ParamValue.prototype.getLiteral = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/**
 * @param {string} value
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.setLiteral = function(value) {
  return jspb.Message.setOneofField(this, 5, proto.vlsir.utils.ParamValue.oneofGroups_[0], value);
};


/**
 * Clears the field making it undefined.
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.clearLiteral = function() {
  return jspb.Message.setOneofField(this, 5, proto.vlsir.utils.ParamValue.oneofGroups_[0], undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.utils.ParamValue.prototype.hasLiteral = function() {
  return jspb.Message.getField(this, 5) != null;
};


/**
 * optional Prefixed prefixed = 6;
 * @return {?proto.vlsir.utils.Prefixed}
 */
proto.vlsir.utils.ParamValue.prototype.getPrefixed = function() {
  return /** @type{?proto.vlsir.utils.Prefixed} */ (
    jspb.Message.getWrapperField(this, proto.vlsir.utils.Prefixed, 6));
};


/**
 * @param {?proto.vlsir.utils.Prefixed|undefined} value
 * @return {!proto.vlsir.utils.ParamValue} returns this
*/
proto.vlsir.utils.ParamValue.prototype.setPrefixed = function(value) {
  return jspb.Message.setOneofWrapperField(this, 6, proto.vlsir.utils.ParamValue.oneofGroups_[0], value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.vlsir.utils.ParamValue} returns this
 */
proto.vlsir.utils.ParamValue.prototype.clearPrefixed = function() {
  return this.setPrefixed(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.vlsir.utils.ParamValue.prototype.hasPrefixed = function() {
  return jspb.Message.getField(this, 6) != null;
};


