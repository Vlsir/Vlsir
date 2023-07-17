/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

goog.provide('proto.vlsir.utils.LibraryMetadata');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');
goog.require('proto.vlsir.utils.AuthorMetadata');


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
proto.vlsir.utils.LibraryMetadata = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.vlsir.utils.LibraryMetadata.repeatedFields_, null);
};
goog.inherits(proto.vlsir.utils.LibraryMetadata, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.vlsir.utils.LibraryMetadata.displayName = 'proto.vlsir.utils.LibraryMetadata';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.vlsir.utils.LibraryMetadata.repeatedFields_ = [10];



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
proto.vlsir.utils.LibraryMetadata.prototype.toObject = function(opt_includeInstance) {
  return proto.vlsir.utils.LibraryMetadata.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.vlsir.utils.LibraryMetadata} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.utils.LibraryMetadata.toObject = function(includeInstance, msg) {
  var f, obj = {
    domain: jspb.Message.getFieldWithDefault(msg, 1, ""),
    cellNamesList: jspb.Message.getRepeatedField(msg, 10),
    author: (f = msg.getAuthor()) && proto.vlsir.utils.AuthorMetadata.toObject(includeInstance, f)
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
 * @return {!proto.vlsir.utils.LibraryMetadata}
 */
proto.vlsir.utils.LibraryMetadata.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.vlsir.utils.LibraryMetadata;
  return proto.vlsir.utils.LibraryMetadata.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.vlsir.utils.LibraryMetadata} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.vlsir.utils.LibraryMetadata}
 */
proto.vlsir.utils.LibraryMetadata.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setDomain(value);
      break;
    case 10:
      var value = /** @type {string} */ (reader.readString());
      msg.addCellNames(value);
      break;
    case 20:
      var value = new proto.vlsir.utils.AuthorMetadata;
      reader.readMessage(value,proto.vlsir.utils.AuthorMetadata.deserializeBinaryFromReader);
      msg.setAuthor(value);
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
proto.vlsir.utils.LibraryMetadata.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.vlsir.utils.LibraryMetadata.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.vlsir.utils.LibraryMetadata} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.vlsir.utils.LibraryMetadata.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getDomain();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getCellNamesList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      10,
      f
    );
  }
  f = message.getAuthor();
  if (f != null) {
    writer.writeMessage(
      20,
      f,
      proto.vlsir.utils.AuthorMetadata.serializeBinaryToWriter
    );
  }
};


/**
 * optional string domain = 1;
 * @return {string}
 */
proto.vlsir.utils.LibraryMetadata.prototype.getDomain = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.vlsir.utils.LibraryMetadata.prototype.setDomain = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * repeated string cell_names = 10;
 * @return {!Array<string>}
 */
proto.vlsir.utils.LibraryMetadata.prototype.getCellNamesList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 10));
};


/** @param {!Array<string>} value */
proto.vlsir.utils.LibraryMetadata.prototype.setCellNamesList = function(value) {
  jspb.Message.setField(this, 10, value || []);
};


/**
 * @param {!string} value
 * @param {number=} opt_index
 */
proto.vlsir.utils.LibraryMetadata.prototype.addCellNames = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 10, value, opt_index);
};


proto.vlsir.utils.LibraryMetadata.prototype.clearCellNamesList = function() {
  this.setCellNamesList([]);
};


/**
 * optional AuthorMetadata author = 20;
 * @return {?proto.vlsir.utils.AuthorMetadata}
 */
proto.vlsir.utils.LibraryMetadata.prototype.getAuthor = function() {
  return /** @type{?proto.vlsir.utils.AuthorMetadata} */ (
    jspb.Message.getWrapperField(this, proto.vlsir.utils.AuthorMetadata, 20));
};


/** @param {?proto.vlsir.utils.AuthorMetadata|undefined} value */
proto.vlsir.utils.LibraryMetadata.prototype.setAuthor = function(value) {
  jspb.Message.setWrapperField(this, 20, value);
};


proto.vlsir.utils.LibraryMetadata.prototype.clearAuthor = function() {
  this.setAuthor(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.vlsir.utils.LibraryMetadata.prototype.hasAuthor = function() {
  return jspb.Message.getField(this, 20) != null;
};


