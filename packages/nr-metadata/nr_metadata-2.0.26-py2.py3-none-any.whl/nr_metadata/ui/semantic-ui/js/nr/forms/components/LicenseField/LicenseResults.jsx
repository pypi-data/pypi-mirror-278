// This file is part of React-Invenio-Deposit
// Copyright (C) 2020 CERN.
// Copyright (C) 2020 Northwestern University.
//
// React-Invenio-Deposit is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import { Item, Header, Radio } from "semantic-ui-react";
import { withState } from "react-searchkit";
import _get from "lodash/get";
import { FastField } from "formik";

export const LicenseResults = withState(
  ({ currentResultsState: results, serializeLicense }) => {
    const serializeLicenseResult =
      serializeLicense ??
      ((result) => ({
        title: result.title,
        id: result.id,
      }));
    return (
      <FastField name="selectedLicense">
        {({ form: { values, setFieldValue } }) => (
          <Item.Group>
            {results.data.hits.map((result) => {
              const { id, title } = result;
              return (
                <Item
                  key={id}
                  onClick={() =>
                    setFieldValue(
                      "selectedLicense",
                      serializeLicenseResult(result)
                    )
                  }
                  className="license-item mb-15"
                >
                  <Radio
                    checked={_get(values, "selectedLicense.id") === id}
                    onChange={() =>
                      setFieldValue(
                        "selectedLicense",
                        serializeLicenseResult(result)
                      )
                    }
                    className="mt-2 mr-5"
                  />
                  <Item.Content className="license-item-content">
                    <Header size="small">{title}</Header>
                  </Item.Content>
                </Item>
              );
            })}
          </Item.Group>
        )}
      </FastField>
    );
  }
);
