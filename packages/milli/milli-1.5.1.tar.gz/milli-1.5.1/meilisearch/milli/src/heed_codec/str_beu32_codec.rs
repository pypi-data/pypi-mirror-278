use std::borrow::Cow;
use std::convert::TryInto;
use std::mem::size_of;
use std::str;

pub struct StrBEU32Codec;

impl<'a> heed::BytesDecode<'a> for StrBEU32Codec {
    type DItem = (&'a str, u32);

    fn bytes_decode(bytes: &'a [u8]) -> Option<Self::DItem> {
        let footer_len = size_of::<u32>();

        if bytes.len() < footer_len {
            return None;
        }

        let (word, bytes) = bytes.split_at(bytes.len() - footer_len);
        let word = str::from_utf8(word).ok()?;
        let pos = bytes.try_into().map(u32::from_be_bytes).ok()?;

        Some((word, pos))
    }
}

impl<'a> heed::BytesEncode<'a> for StrBEU32Codec {
    type EItem = (&'a str, u32);

    fn bytes_encode((word, pos): &Self::EItem) -> Option<Cow<[u8]>> {
        let pos = pos.to_be_bytes();

        let mut bytes = Vec::with_capacity(word.len() + pos.len());
        bytes.extend_from_slice(word.as_bytes());
        bytes.extend_from_slice(&pos[..]);

        Some(Cow::Owned(bytes))
    }
}

pub struct StrBEU16Codec;

impl<'a> heed::BytesDecode<'a> for StrBEU16Codec {
    type DItem = (&'a str, u16);

    fn bytes_decode(bytes: &'a [u8]) -> Option<Self::DItem> {
        let footer_len = size_of::<u16>();

        if bytes.len() < footer_len + 1 {
            return None;
        }

        let (word_plus_nul_byte, bytes) = bytes.split_at(bytes.len() - footer_len);
        let (_, word) = word_plus_nul_byte.split_last()?;
        let word = str::from_utf8(word).ok()?;
        let pos = bytes.try_into().map(u16::from_be_bytes).ok()?;

        Some((word, pos))
    }
}

impl<'a> heed::BytesEncode<'a> for StrBEU16Codec {
    type EItem = (&'a str, u16);

    fn bytes_encode((word, pos): &Self::EItem) -> Option<Cow<[u8]>> {
        let pos = pos.to_be_bytes();

        let mut bytes = Vec::with_capacity(word.len() + 1 + pos.len());
        bytes.extend_from_slice(word.as_bytes());
        bytes.push(0);
        bytes.extend_from_slice(&pos[..]);

        Some(Cow::Owned(bytes))
    }
}
