# typed: false
# frozen_string_literal: true

class AgedUpgrade < Formula
  desc "Upgrade Homebrew packages only after they have been outdated for N days"
  homepage "https://github.com/nhm7/homebrew-aged-upgrade"
  url "https://github.com/nhm7/homebrew-aged-upgrade/archive/refs/tags/v1.1.0.tar.gz"
  sha256 "657e1ce3cfc87aa73efb39eb964e33895ba5a072d18a8933e401e33e49532183"
  version "1.1.0"

  head "https://github.com/nhm7/homebrew-aged-upgrade.git", branch: "main"
  license "MIT"

  depends_on :macos
  uses_from_macos "python3"

  def install
    libexec.install "libexec/brew-aged-upgrade", "libexec/brew-aged-upgrade-core.py"
    bin.write_exec_script libexec/"brew-aged-upgrade"
  end

  test do
    output = shell_output("#{bin}/brew-aged-upgrade help")
    assert_match "start", output
    assert_match "stop", output
    assert_match "status", output
  end
end
