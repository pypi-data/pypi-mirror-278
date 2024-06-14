// This file is part of React-Invenio-Deposit
// Copyright (C) 2020-2021 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
//
// React-Invenio-Deposit is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import PropTypes from "prop-types";
import { getIn, useFormikContext } from "formik";
import { FieldLabel } from "react-invenio-forms";
import { Button, Form, Icon } from "semantic-ui-react";
import { LicenseModal } from "./LicenseModal";
import { LicenseFieldItem } from "./LicenseFieldItem";
import { i18next } from "@translations/nr/i18next";

export const LicenseField = ({
  label,
  labelIcon,
  fieldPath,
  required,
  searchConfig,
  serializeLicense,
  helpText,
}) => {
  const { values, setFieldValue } = useFormikContext();
  const license = getIn(values, fieldPath, {})?.id
    ? getIn(values, fieldPath, {})
    : "";
  const handleLicenseChange = (selectedLicense) => {
    setFieldValue(fieldPath, {id: selectedLicense.id});
  };
  return (
    <Form.Field required={required}>
      <FieldLabel htmlFor={fieldPath} icon={labelIcon} label={label} />
      <label className="helptext">{helpText}</label>
      {license && (
        <LicenseFieldItem
          key={license.id}
          license={license}
          fieldPath={fieldPath}
        />
      )}
      <LicenseModal
        searchConfig={searchConfig}
        initialLicense={license}
        trigger={
          <Button
            type="button"
            key="license"
            icon
            labelPosition="left"
            className="mt-10"
          >
            <Icon name="add" />
            {i18next.t("Choose license")}
          </Button>
        }
        handleLicenseChange={handleLicenseChange}
        serializeLicense={serializeLicense}
      />
    </Form.Field>
  );
};

LicenseField.propTypes = {
  label: PropTypes.string,
  labelIcon: PropTypes.string,
  fieldPath: PropTypes.string.isRequired,
  required: PropTypes.bool,
  searchConfig: PropTypes.object.isRequired,
  serializeLicense: PropTypes.func,
  helpText: PropTypes.string,
};

LicenseField.defaultProps = {
  labelIcon: "drivers license",
  label: i18next.t("License"),
  serializeLicense: undefined,
  required: false,
  helpText: i18next.t(
    "If a Creative Commons license is associated with the resource, select the appropriate license option from the menu. We recommend choosing the latest versions, namely 3.0 Czech and 4.0 International."
  ),
};
