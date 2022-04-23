import React from "react";
import HTMLParser from "html-react-parser";
import { getAsset } from "archive/libs";

interface MarkdownObject {
    content?: string
}

interface MarkdownProps {
    content?: string,
    object?: MarkdownObject,
    asset?: string
}

export const Markdown = ({ content = "", object = null, asset = null }: MarkdownProps) => {
    if(asset != null) {
        object = getAsset(asset);
    }
    if(object != null) {
        content = object.content
    }
    return <article className="markdown-body">{HTMLParser(content)}</article>;
};
