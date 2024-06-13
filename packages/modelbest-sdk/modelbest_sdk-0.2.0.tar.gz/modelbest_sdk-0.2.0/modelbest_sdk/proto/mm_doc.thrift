enum DocType {
    UNKNOWN = 0,
    TXT = 1,
    IMG = 2,
    AUDIO = 3,
    VIDEO = 4,
}

struct MmDoc {
    10: required DocType dtype,        // 当前doc是哪种类型
    20: optional list<i32> token_info,  // encoded tokens for text and audio.
    30: optional list<i32> shape,      // token_info的shape
    40: optional list<bool> mask,      // 一维数组，true表示不需要算loss。大小与shape最后一维大小相同。
    // extra info
    50: optional string docid,         // 当前doc的原始id, 图片类型sample此字段为必填
    70: optional list<string> tag,     // 当前doc的tag，可视化使用.
    // op info
    80: optional string version,
    // reserved cols
    90: optional string reserved_col,  // 为当前doc预留的字段
}

struct MmDocSeq {
    10: required list<MmDoc> doc_seq,
}
