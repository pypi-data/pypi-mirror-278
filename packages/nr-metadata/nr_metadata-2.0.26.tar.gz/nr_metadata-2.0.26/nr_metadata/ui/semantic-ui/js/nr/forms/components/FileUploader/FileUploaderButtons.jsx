import React, { useState } from "react";
import PropTypes from "prop-types";
import { Button, Icon } from "semantic-ui-react";
import FileManagementDialog from "@oarepo/file-manager";
import { FileEditWrapper, FileUploadWrapper } from "./FileUploaderWrappers";
import { useDepositFileApiClient } from "@js/oarepo_ui";
import { i18next } from "@translations/nr/i18next";

export const EditFileButton = ({ fileName, record, allowedFileTypes }) => {
  return (
    <FileEditWrapper
      preactComponent={FileManagementDialog}
      props={{
        config: { record: record },
        autoExtractImagesFromPDFs: false,
        locale: i18next.language,
        startEvent: { event: "edit-file", data: { file_key: fileName } },
        modifyExistingFiles: true,
        allowedFileTypes: allowedFileTypes,
      }}
    />
  );
};

EditFileButton.propTypes = {
  fileName: PropTypes.string.isRequired,
  record: PropTypes.object.isRequired,
  allowedFileTypes: PropTypes.array,
};

export const UploadFileButton = ({
  record,
  handleFilesUpload,
  allowedFileTypes,
}) => {
  return (
    <FileUploadWrapper
      preactComponent={FileManagementDialog}
      props={{
        config: { record: record },
        autoExtractImagesFromPDFs: false,
        locale: i18next.language,
        allowedFileTypes: allowedFileTypes,
        startEvent: null,
        onCompletedUpload: (result) => {
          handleFilesUpload();
        },
        allowedMetaFields: [
          {
            id: "fileNote",
            defaultValue: "",
            isUserInput: true,
          },
        ],
      }}
    />
  );
};

UploadFileButton.propTypes = {
  record: PropTypes.object.isRequired,
  handleFilesUpload: PropTypes.func.isRequired,
  allowedFileTypes: PropTypes.array,
};

export const DeleteFileButton = ({ file, handleFileDeletion }) => {
  const { _delete } = useDepositFileApiClient();
  const [isDeleting, setIsDeleting] = useState(false);
  const handleDelete = async () => {
    setIsDeleting(true);
    _delete(file)
      .then((response) => {
        setIsDeleting(false);
        if (response.status === 204) handleFileDeletion(file);
      })
      .finally(() => {
        setIsDeleting(false);
      });
  };
  return isDeleting ? (
    <Icon loading name="spinner" />
  ) : (
    <Button
      disabled={isDeleting}
      className="transparent"
      type="button"
      onClick={handleDelete}
      aria-label={i18next.t("Delete file")}
    >
      <Icon aria-hidden="true" name="trash alternate" className="m-0" />
    </Button>
  );
};

DeleteFileButton.propTypes = {
  file: PropTypes.object.isRequired,
  handleFileDeletion: PropTypes.func.isRequired,
};
