// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: pb_data_sensor.proto
#pragma warning disable 1591, 0612, 3021
#region Designer generated code

using pb = global::Google.Protobuf;
using pbc = global::Google.Protobuf.Collections;
using pbr = global::Google.Protobuf.Reflection;
using scg = global::System.Collections.Generic;
namespace Com.Richisland.Proto {

  /// <summary>Holder for reflection information generated from pb_data_sensor.proto</summary>
  public static partial class PbDataSensorReflection {

    #region Descriptor
    /// <summary>File descriptor for pb_data_sensor.proto</summary>
    public static pbr::FileDescriptor Descriptor {
      get { return descriptor; }
    }
    private static pbr::FileDescriptor descriptor;

    static PbDataSensorReflection() {
      byte[] descriptorData = global::System.Convert.FromBase64String(
          string.Concat(
            "ChRwYl9kYXRhX3NlbnNvci5wcm90bxIUY29tLnJpY2hpc2xhbmQucHJvdG8a",
            "E3BiX2NvbmZpZ190YWcucHJvdG8i9AEKDnBiX2RhdGFfc2Vuc29yEgwKBG5h",
            "bWUYASABKAkSMAoEdHlwZRgCIAEoDjIiLmNvbS5yaWNoaXNsYW5kLnByb3Rv",
            "LnBiX2RhdGFfdHlwZRIMCgRzaXplGAMgASgFEg0KBXZhbHVlGAQgASgMEgwK",
            "BHRpbWUYBSABKAMSDwoHcXVhbGl0eRgGIAEoBRI0CgZzdGF0dXMYByABKA4y",
            "JC5jb20ucmljaGlzbGFuZC5wcm90by5wYl9kYXRhX3N0YXR1cxIwCgR1bml0",
            "GAggASgOMiIuY29tLnJpY2hpc2xhbmQucHJvdG8ucGJfZGF0YV91bml0Kj4K",
            "DnBiX2RhdGFfc3RhdHVzEggKBEdPT0QQABIHCgNCQUQQARILCgdJTlZBTElE",
            "EAISDAoITk9ORVhJU1QQA2IGcHJvdG8z"));
      descriptor = pbr::FileDescriptor.FromGeneratedCode(descriptorData,
          new pbr::FileDescriptor[] { global::Com.Richisland.Proto.PbConfigTagReflection.Descriptor, },
          new pbr::GeneratedClrTypeInfo(new[] {typeof(global::Com.Richisland.Proto.pb_data_status), }, new pbr::GeneratedClrTypeInfo[] {
            new pbr::GeneratedClrTypeInfo(typeof(global::Com.Richisland.Proto.pb_data_sensor), global::Com.Richisland.Proto.pb_data_sensor.Parser, new[]{ "Name", "Type", "Size", "Value", "Time", "Quality", "Status", "Unit" }, null, null, null)
          }));
    }
    #endregion

  }
  #region Enums
  public enum pb_data_status {
    /// <summary>
    /// 好的
    /// </summary>
    [pbr::OriginalName("GOOD")] Good = 0,
    /// <summary>
    /// 坏的
    /// </summary>
    [pbr::OriginalName("BAD")] Bad = 1,
    /// <summary>
    /// 无效的
    /// </summary>
    [pbr::OriginalName("INVALID")] Invalid = 2,
    /// <summary>
    /// 不存在的
    /// </summary>
    [pbr::OriginalName("NONEXIST")] Nonexist = 3,
  }

  #endregion

  #region Messages
  public sealed partial class pb_data_sensor :PbData, pb::IMessage<pb_data_sensor> {
    private static readonly pb::MessageParser<pb_data_sensor> _parser = new pb::MessageParser<pb_data_sensor>(() => new pb_data_sensor());
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public static pb::MessageParser<pb_data_sensor> Parser { get { return _parser; } }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public static pbr::MessageDescriptor Descriptor {
      get { return global::Com.Richisland.Proto.PbDataSensorReflection.Descriptor.MessageTypes[0]; }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public pb_data_sensor() {
      OnConstruction();
    }

    partial void OnConstruction();

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public pb_data_sensor(pb_data_sensor other) : this() {
      name_ = other.name_;
      type_ = other.type_;
      size_ = other.size_;
      value_ = other.value_;
      time_ = other.time_;
      quality_ = other.quality_;
      status_ = other.status_;
      unit_ = other.unit_;
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public pb_data_sensor Clone() {
      return new pb_data_sensor(this);
    }

    /// <summary>Field number for the "name" field.</summary>
    public const int NameFieldNumber = 1;
    private string name_ = "";
    /// <summary>
    /// 名称
    /// </summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public string Name {
      get { return name_; }
      set {
        name_ = pb::ProtoPreconditions.CheckNotNull(value, "value");
      }
    }

    /// <summary>Field number for the "type" field.</summary>
    public const int TypeFieldNumber = 2;
    private global::Com.Richisland.Proto.pb_data_type type_ = 0;
    /// <summary>
    /// 数据类型
    /// </summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public global::Com.Richisland.Proto.pb_data_type Type {
      get { return type_; }
      set {
        type_ = value;
      }
    }

    /// <summary>Field number for the "size" field.</summary>
    public const int SizeFieldNumber = 3;
    private int size_;
    /// <summary>
    /// 数值字节长度
    /// </summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public int Size {
      get { return size_; }
      set {
        size_ = value;
      }
    }

    /// <summary>Field number for the "value" field.</summary>
    public const int ValueFieldNumber = 4;
    private pb::ByteString value_ = pb::ByteString.Empty;
    /// <summary>
    /// 数值(字节)
    /// </summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public pb::ByteString Value {
      get { return value_; }
      set {
        value_ = pb::ProtoPreconditions.CheckNotNull(value, "value");
      }
    }

    /// <summary>Field number for the "time" field.</summary>
    public const int TimeFieldNumber = 5;
    private long time_;
    /// <summary>
    /// 时间戳
    /// </summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public long Time {
      get { return time_; }
      set {
        time_ = value;
      }
    }

    /// <summary>Field number for the "quality" field.</summary>
    public const int QualityFieldNumber = 6;
    private int quality_;
    /// <summary>
    /// 质量
    /// </summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public int Quality {
      get { return quality_; }
      set {
        quality_ = value;
      }
    }

    /// <summary>Field number for the "status" field.</summary>
    public const int StatusFieldNumber = 7;
    private global::Com.Richisland.Proto.pb_data_status status_ = 0;
    /// <summary>
    /// 状态
    /// </summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public global::Com.Richisland.Proto.pb_data_status Status {
      get { return status_; }
      set {
        status_ = value;
      }
    }

    /// <summary>Field number for the "unit" field.</summary>
    public const int UnitFieldNumber = 8;
    private global::Com.Richisland.Proto.pb_data_unit unit_ = 0;
    /// <summary>
    /// 数值单位
    /// </summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public global::Com.Richisland.Proto.pb_data_unit Unit {
      get { return unit_; }
      set {
        unit_ = value;
      }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override bool Equals(object other) {
      return Equals(other as pb_data_sensor);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public bool Equals(pb_data_sensor other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if (Name != other.Name) return false;
      if (Type != other.Type) return false;
      if (Size != other.Size) return false;
      if (Value != other.Value) return false;
      if (Time != other.Time) return false;
      if (Quality != other.Quality) return false;
      if (Status != other.Status) return false;
      if (Unit != other.Unit) return false;
      return true;
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override int GetHashCode() {
      int hash = 1;
      if (Name.Length != 0) hash ^= Name.GetHashCode();
      if (Type != 0) hash ^= Type.GetHashCode();
      if (Size != 0) hash ^= Size.GetHashCode();
      if (Value.Length != 0) hash ^= Value.GetHashCode();
      if (Time != 0L) hash ^= Time.GetHashCode();
      if (Quality != 0) hash ^= Quality.GetHashCode();
      if (Status != 0) hash ^= Status.GetHashCode();
      if (Unit != 0) hash ^= Unit.GetHashCode();
      return hash;
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void WriteTo(pb::CodedOutputStream output) {
      if (Name.Length != 0) {
        output.WriteRawTag(10);
        output.WriteString(Name);
      }
      if (Type != 0) {
        output.WriteRawTag(16);
        output.WriteEnum((int) Type);
      }
      if (Size != 0) {
        output.WriteRawTag(24);
        output.WriteInt32(Size);
      }
      if (Value.Length != 0) {
        output.WriteRawTag(34);
        output.WriteBytes(Value);
      }
      if (Time != 0L) {
        output.WriteRawTag(40);
        output.WriteInt64(Time);
      }
      if (Quality != 0) {
        output.WriteRawTag(48);
        output.WriteInt32(Quality);
      }
      if (Status != 0) {
        output.WriteRawTag(56);
        output.WriteEnum((int) Status);
      }
      if (Unit != 0) {
        output.WriteRawTag(64);
        output.WriteEnum((int) Unit);
      }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public int CalculateSize() {
      int size = 0;
      if (Name.Length != 0) {
        size += 1 + pb::CodedOutputStream.ComputeStringSize(Name);
      }
      if (Type != 0) {
        size += 1 + pb::CodedOutputStream.ComputeEnumSize((int) Type);
      }
      if (Size != 0) {
        size += 1 + pb::CodedOutputStream.ComputeInt32Size(Size);
      }
      if (Value.Length != 0) {
        size += 1 + pb::CodedOutputStream.ComputeBytesSize(Value);
      }
      if (Time != 0L) {
        size += 1 + pb::CodedOutputStream.ComputeInt64Size(Time);
      }
      if (Quality != 0) {
        size += 1 + pb::CodedOutputStream.ComputeInt32Size(Quality);
      }
      if (Status != 0) {
        size += 1 + pb::CodedOutputStream.ComputeEnumSize((int) Status);
      }
      if (Unit != 0) {
        size += 1 + pb::CodedOutputStream.ComputeEnumSize((int) Unit);
      }
      return size;
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void MergeFrom(pb_data_sensor other) {
      if (other == null) {
        return;
      }
      if (other.Name.Length != 0) {
        Name = other.Name;
      }
      if (other.Type != 0) {
        Type = other.Type;
      }
      if (other.Size != 0) {
        Size = other.Size;
      }
      if (other.Value.Length != 0) {
        Value = other.Value;
      }
      if (other.Time != 0L) {
        Time = other.Time;
      }
      if (other.Quality != 0) {
        Quality = other.Quality;
      }
      if (other.Status != 0) {
        Status = other.Status;
      }
      if (other.Unit != 0) {
        Unit = other.Unit;
      }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            input.SkipLastField();
            break;
          case 10: {
            Name = input.ReadString();
            break;
          }
          case 16: {
            type_ = (global::Com.Richisland.Proto.pb_data_type) input.ReadEnum();
            break;
          }
          case 24: {
            Size = input.ReadInt32();
            break;
          }
          case 34: {
            Value = input.ReadBytes();
            break;
          }
          case 40: {
            Time = input.ReadInt64();
            break;
          }
          case 48: {
            Quality = input.ReadInt32();
            break;
          }
          case 56: {
            status_ = (global::Com.Richisland.Proto.pb_data_status) input.ReadEnum();
            break;
          }
          case 64: {
            unit_ = (global::Com.Richisland.Proto.pb_data_unit) input.ReadEnum();
            break;
          }
        }
      }
    }

  }

  #endregion

}

#endregion Designer generated code
