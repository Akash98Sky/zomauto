import React, { useEffect, useState } from "react";
import fetchData, { PromiseResponse } from "../utils/fetchData";
import {
    Avatar,
    Field,
    Tag,
    TagPicker,
    TagPickerControl,
    TagPickerGroup,
    TagPickerInput,
    TagPickerList,
    TagPickerOption
} from "@fluentui/react-components";

interface Location {
    line1: string;
    line2: string;
}

export function SearchLocations() {
    const [query, setQuery] = useState('');
    const [data, setData] = useState<PromiseResponse<Location[]>>();
    const [locIdx, setLocIdx] = useState<number>();
    const locations = data?.read();

    useEffect(() => {
        if (!query) return;

        const getData = setTimeout(() => {
            try {
                setData(fetchData<Location[]>(`/api/locations?q=${query}`));
            } catch (e) {
                console.log(e);
            }
        }, 2000);

        return () => clearTimeout(getData);
    }, [setData, query]);

    // render this location list in bullet points
    return <Field label="Search Location" style={{ maxWidth: 400 }}>
        <TagPicker
            onOptionSelect={(_, data) => locIdx === parseInt(data.value) ? setLocIdx(undefined) : setLocIdx(parseInt(data.value))}
            selectedOptions={[`${locIdx}`]}
        >
            <TagPickerControl>
                {locIdx !== undefined && (
                    <TagPickerGroup>
                        <Tag
                            key={locIdx}
                            shape="rounded"
                            media={
                                <Avatar aria-hidden name={locations![locIdx].line1} color="colorful" />
                            }
                            value={locIdx.toString()}
                        >
                            {locations![locIdx].line1}
                        </Tag>
                    </TagPickerGroup>
                )}

                <TagPickerInput aria-label="Search Location" onChange={(e) => setQuery(e.target.value)} />
            </TagPickerControl>
            <TagPickerList>
                {
                    locations
                        ?.map((loc, idx) => (
                            <TagPickerOption
                                media={
                                    <Avatar
                                        shape="square"
                                        aria-hidden
                                        name={loc.line1}
                                        color="colorful"
                                    />
                                }
                                value={idx.toString()}
                                key={idx}
                            >
                                {loc.line1 + " - " + loc.line2}
                            </TagPickerOption>
                        )).filter((_, idx) => locIdx !== idx)
                }
            </TagPickerList>
        </TagPicker>
    </Field>;
}